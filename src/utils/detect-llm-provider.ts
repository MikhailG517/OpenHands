/**
 * Auto-detect LLM provider type from base URL
 */

export type LlmProviderType =
  | "openai"
  | "anthropic"
  | "azure"
  | "ollama"
  | "openrouter"
  | "together"
  | "groq"
  | "deepseek"
  | "custom";

interface ProviderDetectionResult {
  type: LlmProviderType;
  confidence: "high" | "medium" | "low";
  displayName: string;
}

interface OllamaModel {
  name: string;
  modified_at?: string;
  size?: number;
}

interface OllamaTagsResponse {
  models: OllamaModel[];
}

interface GenericModel {
  id?: string;
  name?: string;
}

interface GenericModelsResponse {
  models?: GenericModel[];
  data?: GenericModel[];
}

/**
 * Detect provider type from base URL
 */
export function detectProviderFromUrl(
  baseUrl: string,
): ProviderDetectionResult {
  if (!baseUrl) {
    return {
      type: "custom",
      confidence: "low",
      displayName: "Custom",
    };
  }

  const url = baseUrl.toLowerCase().trim();

  // OpenAI
  if (url.includes("api.openai.com") || url.includes("openai.azure.com")) {
    if (url.includes("azure.com")) {
      return {
        type: "azure",
        confidence: "high",
        displayName: "Azure OpenAI",
      };
    }
    return {
      type: "openai",
      confidence: "high",
      displayName: "OpenAI",
    };
  }

  // Anthropic
  if (url.includes("api.anthropic.com") || url.includes("anthropic.com")) {
    return {
      type: "anthropic",
      confidence: "high",
      displayName: "Anthropic",
    };
  }

  // Ollama
  if (
    url.includes("localhost") ||
    url.includes("127.0.0.1") ||
    url.includes(":11434")
  ) {
    return {
      type: "ollama",
      confidence: "medium",
      displayName: "Ollama",
    };
  }

  // OpenRouter
  if (url.includes("openrouter.ai")) {
    return {
      type: "openrouter",
      confidence: "high",
      displayName: "OpenRouter",
    };
  }

  // Together AI
  if (url.includes("together.ai") || url.includes("together.xyz")) {
    return {
      type: "together",
      confidence: "high",
      displayName: "Together AI",
    };
  }

  // Groq
  if (url.includes("groq.com")) {
    return {
      type: "groq",
      confidence: "high",
      displayName: "Groq",
    };
  }

  // DeepSeek
  if (url.includes("deepseek.com")) {
    return {
      type: "deepseek",
      confidence: "high",
      displayName: "DeepSeek",
    };
  }

  // Custom/Unknown
  return {
    type: "custom",
    confidence: "low",
    displayName: "Custom Provider",
  };
}

/**
 * Auto-detect provider and fetch available models
 */
export async function detectProviderAndModels(
  baseUrl: string,
  apiKey?: string,
): Promise<{
  provider: ProviderDetectionResult;
  models: string[];
  error?: string;
}> {
  const provider = detectProviderFromUrl(baseUrl);

  try {
    const models = await fetchModelsFromProvider(
      baseUrl,
      apiKey,
      provider.type,
    );
    return { provider, models };
  } catch (error) {
    return {
      provider,
      models: [],
      error: error instanceof Error ? error.message : "Failed to fetch models",
    };
  }
}

/**
 * Fetch available models from provider
 */
async function fetchModelsFromProvider(
  baseUrl: string,
  apiKey: string | undefined,
  providerType: LlmProviderType,
): Promise<string[]> {
  const url = baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`;

  // Try OpenAI-compatible /v1/models endpoint
  try {
    const response = await fetch(`${url}v1/models`, {
      headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : {},
    });

    if (response.ok) {
      const data = (await response.json()) as GenericModelsResponse;
      if (data.data && Array.isArray(data.data)) {
        return data.data.map((model) => model.id).filter(Boolean) as string[];
      }
    }
  } catch {
    // Continue to next attempt
  }

  // Try Ollama /api/tags endpoint
  if (providerType === "ollama") {
    try {
      const response = await fetch(`${url}api/tags`);
      if (response.ok) {
        const data = (await response.json()) as OllamaTagsResponse;
        if (data.models && Array.isArray(data.models)) {
          return data.models.map((model) => model.name).filter(Boolean);
        }
      }
    } catch {
      // Continue to next attempt
    }
  }

  // Try direct /models endpoint
  try {
    const response = await fetch(`${url}models`, {
      headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : {},
    });

    if (response.ok) {
      const data = (await response.json()) as
        | GenericModel[]
        | GenericModelsResponse;
      if (Array.isArray(data)) {
        return data
          .map((model) => model.id || model.name)
          .filter(Boolean) as string[];
      }
      if (data.models && Array.isArray(data.models)) {
        return data.models
          .map((model) => model.id || model.name)
          .filter(Boolean) as string[];
      }
    }
  } catch {
    // All attempts failed
  }

  throw new Error("Unable to fetch models from this endpoint");
}
