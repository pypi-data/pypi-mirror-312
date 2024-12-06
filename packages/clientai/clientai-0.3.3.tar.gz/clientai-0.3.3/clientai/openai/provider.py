from collections.abc import Iterator
from typing import Any, List, Union, cast

from .._common_types import Message
from ..ai_provider import AIProvider
from ..exceptions import (
    APIError,
    AuthenticationError,
    ClientAIError,
    InvalidRequestError,
    ModelError,
    RateLimitError,
    TimeoutError,
)
from . import OPENAI_INSTALLED
from ._typing import (
    OpenAIClientProtocol,
    OpenAIGenericResponse,
    OpenAIResponse,
    OpenAIStreamResponse,
)

if OPENAI_INSTALLED:
    import openai  # type: ignore
    from openai import AuthenticationError as OpenAIAuthenticationError

    Client = openai.OpenAI
else:
    Client = None  # type: ignore
    OpenAIAuthenticationError = Exception  # type: ignore


class Provider(AIProvider):
    """
    OpenAI-specific implementation of the AIProvider abstract base class.

    This class provides methods to interact with OpenAI's
    models for text generation and chat functionality.

    Attributes:
        client: The OpenAI client used for making API calls.

    Args:
        api_key: The API key for authenticating with OpenAI.

    Raises:
        ImportError: If the OpenAI package is not installed.

    Examples:
        Initialize the OpenAI provider:
        ```python
        provider = Provider(api_key="your-openai-api-key")
        ```
    """

    def __init__(self, api_key: str):
        if not OPENAI_INSTALLED or Client is None:
            raise ImportError(
                "The openai package is not installed. "
                "Please install it with 'pip install clientai[openai]'."
            )
        self.client: OpenAIClientProtocol = cast(
            OpenAIClientProtocol, Client(api_key=api_key)
        )

    def _stream_response(
        self,
        stream: Iterator[OpenAIStreamResponse],
        return_full_response: bool,
    ) -> Iterator[Union[str, OpenAIStreamResponse]]:
        """
        Process the streaming response from OpenAI API.

        Args:
            stream: The stream of responses from OpenAI API.
            return_full_response: If True, yield full response objects.

        Yields:
            Union[str, OpenAIStreamResponse]: Processed content or full
                                              response objects.
        """
        for chunk in stream:
            if return_full_response:
                yield chunk
            else:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

    def _map_exception_to_clientai_error(self, e: Exception) -> ClientAIError:
        """
        Maps an OpenAI exception to the appropriate ClientAI exception.

        Args:
            e (Exception): The exception caught during the API call.

        Raises:
            ClientAIError: An instance of the appropriate ClientAI exception.
        """
        error_message = str(e)
        status_code = None

        if hasattr(e, "status_code"):
            status_code = e.status_code
        else:
            try:
                status_code = int(
                    error_message.split("Error code: ")[1].split(" -")[0]
                )
            except (IndexError, ValueError):
                pass

        if (
            isinstance(e, OpenAIAuthenticationError)
            or "incorrect api key" in error_message.lower()
        ):
            return AuthenticationError(
                error_message, status_code, original_error=e
            )
        elif (
            isinstance(e, openai.OpenAIError)
            or "error code:" in error_message.lower()
        ):
            if status_code == 429 or "rate limit" in error_message.lower():
                return RateLimitError(
                    error_message, status_code, original_error=e
                )
            elif status_code == 404 or "not found" in error_message.lower():
                return ModelError(error_message, status_code, original_error=e)
            elif status_code == 400 or "invalid" in error_message.lower():
                return InvalidRequestError(
                    error_message, status_code, original_error=e
                )
            elif status_code == 408 or "timeout" in error_message.lower():
                return TimeoutError(
                    error_message, status_code, original_error=e
                )
            elif status_code and status_code >= 500:
                return APIError(error_message, status_code, original_error=e)

        return ClientAIError(error_message, status_code, original_error=e)

    def generate_text(
        self,
        prompt: str,
        model: str,
        return_full_response: bool = False,
        stream: bool = False,
        json_output: bool = False,
        **kwargs: Any,
    ) -> OpenAIGenericResponse:
        """
        Generate text based on a given prompt using a specified OpenAI model.

        Args:
            prompt: The input prompt for text generation.
            model: The name or identifier of the OpenAI model to use.
            return_full_response: If True, return the full response object.
                If False, return only the generated text. Defaults to False.
            stream: If True, return an iterator for streaming responses.
                Defaults to False.
            json_output: If True, format the response as valid JSON using
                OpenAI's native JSON mode. The prompt should specify the
                desired JSON structure. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            OpenAIGenericResponse: The generated text, full response object,
            or an iterator for streaming responses.

        Raises:
            ClientAIError: If an error occurs during the API call.

        Examples:
            Generate text (text only):
            ```python
            response = provider.generate_text(
                "Explain the theory of relativity",
                model="gpt-3.5-turbo",
            )
            print(response)
            ```

            Generate text (full response):
            ```python
            response = provider.generate_text(
                "Explain the theory of relativity",
                model="gpt-3.5-turbo",
                return_full_response=True
            )
            print(response.choices[0].message.content)
            ```

            Generate text (streaming):
            ```python
            for chunk in provider.generate_text(
                "Explain the theory of relativity",
                model="gpt-3.5-turbo",
                stream=True
            ):
                print(chunk, end="", flush=True)
            ```

            Generate JSON output:
            ```python
            response = provider.generate_text(
                '''Generate a user profile with the following structure:
                {
                    "name": "A random name",
                    "age": "A random age between 20-80",
                    "occupation": "A random occupation"
                }''',
                model="gpt-3.5-turbo",
                json_output=True
            )
            print(response)  # Will be valid JSON
            ```
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            completion_kwargs = {
                "model": model,
                "messages": messages,
                "stream": stream,
            }
            if json_output:
                completion_kwargs["response_format"] = {"type": "json_object"}
            completion_kwargs.update(kwargs)

            response = self.client.chat.completions.create(**completion_kwargs)

            if stream:
                return cast(
                    OpenAIGenericResponse,
                    self._stream_response(
                        cast(Iterator[OpenAIStreamResponse], response),
                        return_full_response,
                    ),
                )
            else:
                response = cast(OpenAIResponse, response)
                if return_full_response:
                    return response
                else:
                    return response.choices[0].message.content

        except Exception as e:
            raise self._map_exception_to_clientai_error(e)

    def chat(
        self,
        messages: List[Message],
        model: str,
        return_full_response: bool = False,
        stream: bool = False,
        json_output: bool = False,
        **kwargs: Any,
    ) -> OpenAIGenericResponse:
        """
        Engage in a chat conversation using a specified OpenAI model.

        Args:
            messages: A list of message dictionaries, each containing
                      'role' and 'content'.
            model: The name or identifier of the OpenAI model to use.
            return_full_response: If True, return the full response object.
                If False, return only the generated text. Defaults to False.
            stream: If True, return an iterator for streaming responses.
                Defaults to False.
            json_output: If True, format the response as valid JSON using
                OpenAI's native JSON mode. The messages should specify the
                desired JSON structure. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            OpenAIGenericResponse: The chat response, full response object,
            or an iterator for streaming responses.

        Raises:
            ClientAIError: If an error occurs during the API call.

        Examples:
            Chat (message content only):
            ```python
            messages = [
                {"role": "user", "content": "What is the capital of France?"},
                {"role": "assistant", "content": "The capital is Paris."},
                {"role": "user", "content": "What is its population?"}
            ]
            response = provider.chat(
                messages,
                model="gpt-3.5-turbo",
            )
            print(response)
            ```

            Chat (full response):
            ```python
            response = provider.chat(
                messages,
                model="gpt-3.5-turbo",
                return_full_response=True
            )
            print(response.choices[0].message.content)
            ```

            Chat (streaming):
            ```python
            for chunk in provider.chat(
                messages,
                model="gpt-3.5-turbo",
                stream=True
            ):
                print(chunk, end="", flush=True)
            ```

            Chat with JSON output:
            ```python
            messages = [
                {"role": "user", "content": '''Generate a user profile with:
                {
                    "name": "A random name",
                    "age": "A random age between 20-80",
                    "occupation": "A random occupation"
                }'''}
            ]
            response = provider.chat(
                messages,
                model="gpt-3.5-turbo",
                json_output=True
            )
            print(response)  # Will be valid JSON
            ```
        """
        try:
            completion_kwargs = {
                "model": model,
                "messages": messages,
                "stream": stream,
            }
            if json_output:
                completion_kwargs["response_format"] = {"type": "json_object"}
            completion_kwargs.update(kwargs)

            response = self.client.chat.completions.create(**completion_kwargs)

            if stream:
                return cast(
                    OpenAIGenericResponse,
                    self._stream_response(
                        cast(Iterator[OpenAIStreamResponse], response),
                        return_full_response,
                    ),
                )
            else:
                response = cast(OpenAIResponse, response)
                if return_full_response:
                    return response
                else:
                    return response.choices[0].message.content

        except Exception as e:
            raise self._map_exception_to_clientai_error(e)
