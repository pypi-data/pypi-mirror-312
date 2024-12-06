# Copyright 2023 The Langfun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Language models from OpenAI."""

import collections
import functools
import os
from typing import Annotated, Any

import langfun.core as lf
from langfun.core import modalities as lf_modalities
import pyglove as pg

try:
  import openai  # pylint: disable=g-import-not-at-top

  if hasattr(openai, 'error'):
    # For lower versions.
    ServiceUnavailableError = openai.error.ServiceUnavailableError
    RateLimitError = openai.error.RateLimitError
    APITimeoutError = (
        openai.error.APIError,
        '.*The server had an error processing your request'
    )
  else:
    # For higher versions.
    ServiceUnavailableError = getattr(openai, 'InternalServerError')
    RateLimitError = getattr(openai, 'RateLimitError')
    APITimeoutError = getattr(openai, 'APITimeoutError')
except ImportError:
  openai = None


# From https://platform.openai.com/settings/organization/limits
_DEFAULT_TPM = 250000
_DEFAULT_RPM = 3000

SUPPORTED_MODELS_AND_SETTINGS = {
    # Models from https://platform.openai.com/docs/models
    # RPM is from https://platform.openai.com/docs/guides/rate-limits
    # o1 (preview) models.
    # Pricing in US dollars, from https://openai.com/api/pricing/
    # as of 2024-10-10.
    'o1-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.015,
        cost_per_1k_output_tokens=0.06,
    ),
    'o1-preview-2024-09-12': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.015,
        cost_per_1k_output_tokens=0.06,
    ),
    'o1-mini': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.003,
        cost_per_1k_output_tokens=0.012,
    ),
    'o1-mini-2024-09-12': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.003,
        cost_per_1k_output_tokens=0.012,
    ),
    # GPT-4o models
    'gpt-4o-mini': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.00015,
        cost_per_1k_output_tokens=0.0006,
    ),
    'gpt-4o-mini-2024-07-18': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.00015,
        cost_per_1k_output_tokens=0.0006,
    ),
    'gpt-4o': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.0025,
        cost_per_1k_output_tokens=0.01,
    ),
    'gpt-4o-2024-11-20': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.0025,
        cost_per_1k_output_tokens=0.01,
    ),
    'gpt-4o-2024-08-06': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.0025,
        cost_per_1k_output_tokens=0.01,
    ),
    'gpt-4o-2024-05-13': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=5000000,
        cost_per_1k_input_tokens=0.005,
        cost_per_1k_output_tokens=0.015,
    ),
    # GPT-4-Turbo models
    'gpt-4-turbo': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-turbo-2024-04-09': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-turbo-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-0125-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-1106-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-vision-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    'gpt-4-1106-vision-preview': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
    ),
    # GPT-4 models
    'gpt-4': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.03,
        cost_per_1k_output_tokens=0.06,
    ),
    'gpt-4-0613': pg.Dict(
        in_service=False,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.03,
        cost_per_1k_output_tokens=0.06,
    ),
    'gpt-4-0314': pg.Dict(
        in_service=False,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.03,
        cost_per_1k_output_tokens=0.06,
    ),
    'gpt-4-32k': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.06,
        cost_per_1k_output_tokens=0.12,
    ),
    'gpt-4-32k-0613': pg.Dict(
        in_service=False,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.06,
        cost_per_1k_output_tokens=0.12,
    ),
    'gpt-4-32k-0314': pg.Dict(
        in_service=False,
        rpm=10000,
        tpm=300000,
        cost_per_1k_input_tokens=0.06,
        cost_per_1k_output_tokens=0.12,
    ),
    # GPT-3.5-Turbo models
    'gpt-3.5-turbo': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.0005,
        cost_per_1k_output_tokens=0.0015,
    ),
    'gpt-3.5-turbo-0125': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.0005,
        cost_per_1k_output_tokens=0.0015,
    ),
    'gpt-3.5-turbo-1106': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.001,
        cost_per_1k_output_tokens=0.002,
    ),
    'gpt-3.5-turbo-0613': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.0015,
        cost_per_1k_output_tokens=0.002,
    ),
    'gpt-3.5-turbo-0301': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.0015,
        cost_per_1k_output_tokens=0.002,
    ),
    'gpt-3.5-turbo-16k': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.003,
        cost_per_1k_output_tokens=0.004,
    ),
    'gpt-3.5-turbo-16k-0613': pg.Dict(
        in_service=True,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.003,
        cost_per_1k_output_tokens=0.004,
    ),
    'gpt-3.5-turbo-16k-0301': pg.Dict(
        in_service=False,
        rpm=10000,
        tpm=2000000,
        cost_per_1k_input_tokens=0.003,
        cost_per_1k_output_tokens=0.004,
    ),
    # GPT-3.5 models
    'text-davinci-003': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'text-davinci-002': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'code-davinci-002': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    # GPT-3 instruction-tuned models
    'text-curie-001': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'text-babbage-001': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM,
    ),
    'text-ada-001': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM,
    ),
    'davinci': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM,
    ),
    'curie': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'babbage': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'ada': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    # GPT-3 base models
    'babbage-002': pg.Dict(
        in_service=False,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
    'davinci-002': pg.Dict(
        in_service=True,
        rpm=_DEFAULT_RPM,
        tpm=_DEFAULT_TPM
    ),
}


@lf.use_init_args(['model'])
class OpenAI(lf.LanguageModel):
  """OpenAI model."""

  model: pg.typing.Annotated[
      pg.typing.Enum(
          pg.MISSING_VALUE, list(SUPPORTED_MODELS_AND_SETTINGS.keys())
      ),
      'The name of the model to use.',
  ] = 'gpt-3.5-turbo'

  multimodal: Annotated[
      bool,
      'Whether this model has multimodal support.'
  ] = False

  api_key: Annotated[
      str | None,
      (
          'API key. If None, the key will be read from environment variable '
          "'OPENAI_API_KEY'."
      ),
  ] = None

  organization: Annotated[
      str | None,
      (
          'Organization. If None, the key will be read from environment '
          "variable 'OPENAI_ORGANIZATION'. Based on the value, usages from "
          "these API requests will count against the organization's quota. "
      ),
  ] = None

  def _on_bound(self):
    super()._on_bound()
    self.__dict__.pop('_api_initialized', None)
    if openai is None:
      raise RuntimeError(
          'Please install "langfun[llm-openai]" to use OpenAI models.'
      )

  @functools.cached_property
  def _api_initialized(self):
    api_key = self.api_key or os.environ.get('OPENAI_API_KEY', None)
    if not api_key:
      raise ValueError(
          'Please specify `api_key` during `__init__` or set environment '
          'variable `OPENAI_API_KEY` with your OpenAI API key.'
      )
    openai.api_key = api_key
    org = self.organization or os.environ.get('OPENAI_ORGANIZATION', None)
    if org:
      openai.organization = org
    return True

  @property
  def model_id(self) -> str:
    """Returns a string to identify the model."""
    return f'OpenAI({self.model})'

  @property
  def max_concurrency(self) -> int:
    rpm = SUPPORTED_MODELS_AND_SETTINGS[self.model].get('rpm', 0)
    tpm = SUPPORTED_MODELS_AND_SETTINGS[self.model].get('tpm', 0)
    return self.rate_to_max_concurrency(
        requests_per_min=rpm, tokens_per_min=tpm
    )

  def estimate_cost(
      self,
      num_input_tokens: int,
      num_output_tokens: int
  ) -> float | None:
    """Estimate the cost based on usage."""
    cost_per_1k_input_tokens = SUPPORTED_MODELS_AND_SETTINGS[self.model].get(
        'cost_per_1k_input_tokens', None
    )
    cost_per_1k_output_tokens = SUPPORTED_MODELS_AND_SETTINGS[self.model].get(
        'cost_per_1k_output_tokens', None
    )
    if cost_per_1k_output_tokens is None or cost_per_1k_input_tokens is None:
      return None
    return (
        cost_per_1k_input_tokens * num_input_tokens
        + cost_per_1k_output_tokens * num_output_tokens
    ) / 1000

  @classmethod
  def dir(cls):
    assert openai is not None
    return openai.Model.list()

  @property
  def is_chat_model(self):
    """Returns True if the model is a chat model."""
    return self.model.startswith(('o1', 'gpt-4', 'gpt-3.5-turbo'))

  def _get_request_args(
      self, options: lf.LMSamplingOptions) -> dict[str, Any]:
    # Reference:
    # https://platform.openai.com/docs/api-reference/completions/create
    # NOTE(daiyip): options.top_k is not applicable.
    args = dict(
        n=options.n,
        stream=False,
        timeout=self.timeout,
        top_logprobs=options.top_logprobs,
    )
    if options.logprobs:
      # Reasoning models (o1 series) does not support `logprobs` by 2024/09/12.
      if self.model.startswith('o1-'):
        raise RuntimeError('`logprobs` is not supported on {self.model!r}.')
      args['logprobs'] = options.logprobs

    # Completion and ChatCompletion uses different parameter name for model.
    args['model' if self.is_chat_model else 'engine'] = self.model

    if options.temperature is not None:
      args['temperature'] = options.temperature
    if options.max_tokens is not None:
      args['max_tokens'] = options.max_tokens
    if options.top_p is not None:
      args['top_p'] = options.top_p
    if options.stop:
      args['stop'] = options.stop
    if options.random_seed is not None:
      args['seed'] = options.random_seed
    return args

  def _sample(self, prompts: list[lf.Message]) -> list[lf.LMSamplingResult]:
    assert self._api_initialized
    if self.is_chat_model:
      return self._chat_complete_batch(prompts)
    else:
      return self._complete_batch(prompts)

  def _complete_batch(
      self, prompts: list[lf.Message]
  ) -> list[lf.LMSamplingResult]:

    def _open_ai_completion(prompts):
      assert openai is not None
      response = openai.Completion.create(
          prompt=[p.text for p in prompts],
          **self._get_request_args(self.sampling_options),
      )
      # Parse response.
      samples_by_index = collections.defaultdict(list)
      for choice in response.choices:
        samples_by_index[choice.index].append(
            lf.LMSample(choice.text.strip(), score=choice.logprobs or 0.0)
        )

      n = len(samples_by_index)
      estimated_cost = self.estimate_cost(
          num_input_tokens=response.usage.prompt_tokens,
          num_output_tokens=response.usage.completion_tokens,
      )
      usage = lf.LMSamplingUsage(
          prompt_tokens=response.usage.prompt_tokens // n,
          completion_tokens=response.usage.completion_tokens // n,
          total_tokens=response.usage.total_tokens // n,
          estimated_cost=(
              None if estimated_cost is None else (estimated_cost // n)
          )
      )
      return [
          lf.LMSamplingResult(samples_by_index[index], usage=usage)
          for index in sorted(samples_by_index.keys())
      ]

    return self._parallel_execute_with_currency_control(
        _open_ai_completion,
        [prompts],
        retry_on_errors=(
            ServiceUnavailableError,
            RateLimitError,
            APITimeoutError,
        ),
    )[0]

  def _chat_complete_batch(
      self, prompts: list[lf.Message]
  ) -> list[lf.LMSamplingResult]:
    def _content_from_message(message: lf.Message):
      if self.multimodal:
        content = []
        for chunk in message.chunk():
          if isinstance(chunk, str):
            item = dict(type='text', text=chunk)
          elif isinstance(chunk, lf_modalities.Image):
            if chunk.uri and chunk.uri.lower().startswith(
                ('http:', 'https:', 'ftp:')
            ):
              uri = chunk.uri
            else:
              uri = chunk.content_uri
            item = dict(type='image_url', image_url=dict(url=uri))
          else:
            raise ValueError(f'Unsupported modality object: {chunk!r}.')
          content.append(item)
      else:
        content = message.text
      return content

    def _open_ai_chat_completion(prompt: lf.Message):
      request_args = self._get_request_args(self.sampling_options)
      # Users could use `metadata_json_schema` to pass additional
      # request arguments.
      json_schema = prompt.metadata.get('json_schema')
      if json_schema is not None:
        if not isinstance(json_schema, dict):
          raise ValueError(
              f'`json_schema` must be a dict, got {json_schema!r}.'
          )
        if 'title' not in json_schema:
          raise ValueError(
              f'The root of `json_schema` must have a `title` field, '
              f'got {json_schema!r}.'
          )
        request_args.update(
            response_format=dict(
                type='json_schema',
                json_schema=dict(
                    schema=json_schema,
                    name=json_schema['title'],
                    strict=True,
                )
            )
        )
        prompt.metadata.formatted_text = (
            prompt.text
            + '\n\n [RESPONSE FORMAT (not part of prompt)]\n'
            + pg.to_json_str(request_args['response_format'], json_indent=2)
        )

      # Prepare messages.
      messages = []
      # Users could use `metadata_system_message` to pass system message.
      system_message = prompt.metadata.get('system_message')
      if system_message:
        system_message = lf.SystemMessage.from_value(system_message)
        messages.append(
            dict(role='system', content=_content_from_message(system_message))
        )
      messages.append(dict(role='user', content=_content_from_message(prompt)))

      assert openai is not None
      response = openai.ChatCompletion.create(messages=messages, **request_args)

      samples = []
      for choice in response.choices:
        logprobs = None
        choice_logprobs = getattr(choice, 'logprobs', None)
        if choice_logprobs:
          logprobs = [
              (
                  t.token,
                  t.logprob,
                  [(tt.token, tt.logprob) for tt in t.top_logprobs],
              )
              for t in choice_logprobs.content
          ]
        samples.append(
            lf.LMSample(
                choice.message.content,
                score=0.0,
                logprobs=logprobs,
            )
        )

      return lf.LMSamplingResult(
          samples=samples,
          usage=lf.LMSamplingUsage(
              prompt_tokens=response.usage.prompt_tokens,
              completion_tokens=response.usage.completion_tokens,
              total_tokens=response.usage.total_tokens,
              estimated_cost=self.estimate_cost(
                  num_input_tokens=response.usage.prompt_tokens,
                  num_output_tokens=response.usage.completion_tokens,
              )
          ),
      )

    return self._parallel_execute_with_currency_control(
        _open_ai_chat_completion,
        prompts,
        retry_on_errors=(
            ServiceUnavailableError,
            RateLimitError,
            APITimeoutError
        ),
    )


class GptO1Preview(OpenAI):
  """GPT-O1."""
  model = 'o1-preview'


class GptO1Preview_20240912(OpenAI):   # pylint: disable=invalid-name
  """GPT O1."""
  model = 'o1-preview-2024-09-12'


class GptO1Mini(OpenAI):
  """GPT O1-mini."""
  model = 'o1-mini'


class GptO1Mini_20240912(OpenAI):   # pylint: disable=invalid-name
  """GPT O1-mini."""
  model = 'o1-mini-2024-09-12'


class Gpt4(OpenAI):
  """GPT-4."""
  model = 'gpt-4'


class Gpt4Turbo(Gpt4):
  """GPT-4 Turbo with 128K context window. Knowledge up to Dec. 2023."""
  model = 'gpt-4-turbo'
  multimodal = True


class Gpt4Turbo_20240409(Gpt4Turbo):  # pylint:disable=invalid-name
  """GPT-4 Turbo with 128K context window. Knowledge up to Dec. 2023."""
  model = 'gpt-4-turbo-2024-04-09'
  multimodal = True


class Gpt4TurboPreview(Gpt4):
  """GPT-4 Turbo Preview with 128k context window. Knowledge up to Dec. 2023."""
  model = 'gpt-4-turbo-preview'


class Gpt4TurboPreview_20240125(Gpt4TurboPreview):  # pylint: disable=invalid-name
  """GPT-4 Turbo Preview with 128k context window. Knowledge up to Dec. 2023."""
  model = 'gpt-4-0125-preview'


class Gpt4TurboPreview_20231106(Gpt4TurboPreview):  # pylint: disable=invalid-name
  """GPT-4 Turbo Preview with 128k context window. Knowledge up to Apr. 2023."""
  model = 'gpt-4-1106-preview'


class Gpt4VisionPreview(Gpt4):
  """GPT-4 Turbo vision preview. 128k context window. Knowledge to Apr. 2023."""
  model = 'gpt-4-vision-preview'
  multimodal = True


class Gpt4VisionPreview_20231106(Gpt4):  # pylint: disable=invalid-name
  """GPT-4 Turbo vision preview. 128k context window. Knowledge to Apr. 2023."""
  model = 'gpt-4-1106-vision-preview'


class Gpt4_20230613(Gpt4):    # pylint:disable=invalid-name
  """GPT-4 @20230613. 8K context window. Knowledge up to 9-2021."""
  model = 'gpt-4-0613'


class Gpt4_32K(Gpt4):       # pylint:disable=invalid-name
  """Latest GPT-4 with 32K context window."""
  model = 'gpt-4-32k'


class Gpt4_32K_20230613(Gpt4_32K):    # pylint:disable=invalid-name
  """GPT-4 @20230613. 32K context window. Knowledge up to 9-2021."""
  model = 'gpt-4-32k-0613'


class Gpt4oMini(OpenAI):
  """GPT-4o Mini."""
  model = 'gpt-4o-mini'
  multimodal = True


class Gpt4oMini_20240718(OpenAI):  # pylint:disable=invalid-name
  """GPT-4o Mini."""
  model = 'gpt-4o-mini-2024-07-18'
  multimodal = True


class Gpt4o(OpenAI):
  """GPT-4o."""
  model = 'gpt-4o'
  multimodal = True


class Gpt4o_20241120(OpenAI):     # pylint:disable=invalid-name
  """GPT-4o version 2024-11-20."""
  model = 'gpt-4o-2024-11-20'
  multimodal = True


class Gpt4o_20240806(OpenAI):     # pylint:disable=invalid-name
  """GPT-4o version 2024-08-06."""
  model = 'gpt-4o-2024-08-06'
  multimodal = True


class Gpt4o_20240513(OpenAI):     # pylint:disable=invalid-name
  """GPT-4o version 2024-05-13."""
  model = 'gpt-4o-2024-05-13'
  multimodal = True


class Gpt35(OpenAI):
  """GPT-3.5. 4K max tokens, trained up on data up to Sep, 2021."""
  model = 'text-davinci-003'


class Gpt35Turbo(Gpt35):
  """Most capable GPT-3.5 model, 10x cheaper than GPT35 (text-davinci-003)."""
  model = 'gpt-3.5-turbo'


class Gpt35Turbo_20240125(Gpt35Turbo):   # pylint:disable=invalid-name
  """GPT-3.5 Turbo @20240125. 16K context window. Knowledge up to 09/2021."""
  model = 'gpt-3.5-turbo-0125'


class Gpt35Turbo_20231106(Gpt35Turbo):   # pylint:disable=invalid-name
  """Gpt3.5 Turbo @20231106. 16K context window. Knowledge up to 09/2021."""
  model = 'gpt-3.5-turbo-1106'


class Gpt35Turbo_20230613(Gpt35Turbo):   # pylint:disable=invalid-name
  """Gpt3.5 Turbo snapshot at 2023/06/13, with 4K context window size."""
  model = 'gpt-3.5-turbo-0613'


class Gpt35Turbo16K(Gpt35Turbo):
  """Latest GPT-3.5 model with 16K context window size."""
  model = 'gpt-3.5-turbo-16k'


class Gpt35Turbo16K_20230613(Gpt35Turbo):   # pylint:disable=invalid-name
  """Gtp 3.5 Turbo 16K 0613."""
  model = 'gpt-3.5-turbo-16k-0613'


class Gpt3(OpenAI):
  """Most capable GPT-3 model (Davinci) 2K context window size.

  All GPT3 models have 2K max tokens and trained on data up to Oct 2019.
  """
  model = 'davinci'


class Gpt3Curie(Gpt3):
  """Very capable, but faster and lower cost than Davici."""
  model = 'curie'


class Gpt3Babbage(Gpt3):
  """Capable of straightforward tasks, very fast and low cost."""
  model = 'babbage'


class Gpt3Ada(Gpt3):
  """Capable of very simple tasks, the fastest/lowest cost among GPT3 models."""
  model = 'ada'
