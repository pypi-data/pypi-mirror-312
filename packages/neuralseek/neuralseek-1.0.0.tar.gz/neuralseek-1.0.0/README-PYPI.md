# neuralseek

Developer-friendly & type-safe Python SDK specifically catered to leverage *neuralseek* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=neuralseek&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<!-- Start Summary [summary] -->
## Summary

NeuralSeek: NeuralSeek - The business LLM accelerator

For more information about the API: [Documentation](https://neuralseek.com/documentation)
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [neuralseek](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#neuralseek)
  * [SDK Installation](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#authentication)
  * [Available Resources and Operations](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#available-resources-and-operations)
  * [Server-sent event streaming](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#server-sent-event-streaming)
  * [File uploads](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#file-uploads)
  * [Retries](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#retries)
  * [Error Handling](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#error-handling)
  * [Server Selection](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#custom-http-client)
  * [Debugging](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#debugging)
* [Development](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#development)
  * [Maturity](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#maturity)
  * [Contributions](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install neuralseek
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add neuralseek
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from neuralseek import Neuralseek
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.execute()

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from neuralseek import Neuralseek
import os

async def main():
    async with Neuralseek(
        api_key=os.getenv("NEURALSEEK_API_KEY", ""),
    ) as s:
        res = await s.seek.execute_async()

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type   | Scheme  | Environment Variable |
| --------- | ------ | ------- | -------------------- |
| `api_key` | apiKey | API key | `NEURALSEEK_API_KEY` |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from neuralseek import Neuralseek
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.execute()

    if res is not None:
        # handle response
        pass

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [analytics](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/analytics/README.md)

* [retrieve](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/analytics/README.md#retrieve) - Instance Analytics

### [answer_ratings](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/answerratings/README.md)

* [get_average](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/answerratings/README.md#get_average) - Get the average user ratings for an answer

### [categorize](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/categorize/README.md)

* [execute](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/categorize/README.md#execute) - Categorize text into an Intent & Category

### [extract_entities](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/extractentities/README.md)

* [post](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/extractentities/README.md#post) - Extract entitites from text

### [find_pii](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/findpii/README.md)

* [detect](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/findpii/README.md#detect) - Find PII in a user utterance

### [identify_language](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/identifylanguage/README.md)

* [identify](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/identifylanguage/README.md#identify) - Identify the source language

### [identify_language_json](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/identifylanguagejson/README.md)

* [identify](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/identifylanguagejson/README.md#identify) - Identify the source language (JSON)

### [key_check](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/keycheck/README.md)

* [post](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/keycheck/README.md#post) - Validate an api key

### [logs](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/logs/README.md)

* [retrieve](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/logs/README.md#retrieve) - Instance Logs

### [maistro](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/maistro/README.md)

* [execute](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/maistro/README.md#execute) - Run mAistro NTL or template
* [stream](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/maistro/README.md#stream) - Stream mAIstro NTL or a template


### [one_time_password](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/onetimepassword/README.md)

* [create](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/onetimepassword/README.md#create) - Create a One Time Password

### [rate](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/rate/README.md)

* [submit](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/rate/README.md#submit) - Rate an answer

### [score](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/score/README.md)

* [post](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/score/README.md#post) - Run the Semantic Scoring model on text against an array of passages

### [seek](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/seeksdk/README.md)

* [execute](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/seeksdk/README.md#execute) - Seek an answer from NeuralSeek
* [stream](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/seeksdk/README.md#stream) - Stream a Seek an answer from NeuralSeek

### [service_test](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/servicetest/README.md)

* [check](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/servicetest/README.md#check) - Service check

### [test_questions](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/testquestions/README.md)

* [upload_multipart](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/testquestions/README.md#upload_multipart) - Test questions via batch upload
* [upload_json](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/testquestions/README.md#upload_json) - Test questions via batch upload

### [test_results](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/testresults/README.md)

* [get](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/testresults/README.md#get) - Get Test Results

### [train](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/train/README.md)

* [post](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/train/README.md#post) - Submit KnowledgeBase Training

### [translate](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translate/README.md)

* [execute](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translate/README.md#execute) - Translate text into a desired language

### [translation_glossary](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translationglossary/README.md)

* [add_multipart](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translationglossary/README.md#add_multipart) - Add custom translations
* [add_json](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translationglossary/README.md#add_json) - Add custom translations
* [delete](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/translationglossary/README.md#delete) - Delete the custom translations

### [user_data](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/userdata/README.md)

* [delete](https://github.com/CerebralBlue/neuralseek-python-sdk/blob/master/docs/sdks/userdata/README.md#delete) - Delete all user data

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.  

The stream is also a [Context Manager][context-manager] and can be used with the `with` statement and will close the
underlying connection when the context is exited.

```python
from neuralseek import Neuralseek
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.stream()

    if res is not None:
        with res as event_stream:
            for event in event_stream:
                # handle event
                print(event, flush=True)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://book.pythontips.com/en/latest/generators.html
[context-manager]: https://book.pythontips.com/en/latest/context_managers.html
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
from neuralseek import Neuralseek
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    s.translation_glossary.add_multipart()

    # Use the SDK ...

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from neuralseek import Neuralseek
from neuralseek.utils import BackoffStrategy, RetryConfig
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.execute(,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    if res is not None:
        # handle response
        pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from neuralseek import Neuralseek
from neuralseek.utils import BackoffStrategy, RetryConfig
import os

with Neuralseek(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.execute()

    if res is not None:
        # handle response
        pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `execute_async` method may raise the following exceptions:

| Error Type      | Status Code | Content Type |
| --------------- | ----------- | ------------ |
| models.APIError | 4XX, 5XX    | \*/\*        |

### Example

```python
from neuralseek import Neuralseek, models
import os

with Neuralseek(
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = None
    try:
        res = s.seek.execute()

        if res is not None:
            # handle response
            pass

    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Server Variables

The default server `https://api.neuralseek.com/v1/{instance}` contains variables and is set to `https://api.neuralseek.com/v1/demo` by default. To override default values, the following parameters are available when initializing the SDK client instance:
 * `instance: str`

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from neuralseek import Neuralseek
import os

with Neuralseek(
    server_url="https://api.neuralseek.com/v1/demo",
    api_key=os.getenv("NEURALSEEK_API_KEY", ""),
) as s:
    res = s.seek.execute()

    if res is not None:
        # handle response
        pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from neuralseek import Neuralseek
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Neuralseek(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from neuralseek import Neuralseek
from neuralseek.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Neuralseek(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from neuralseek import Neuralseek
import logging

logging.basicConfig(level=logging.DEBUG)
s = Neuralseek(debug_logger=logging.getLogger("neuralseek"))
```

You can also enable a default debug logger by setting an environment variable `NEURALSEEK_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=neuralseek&utm_campaign=python)
