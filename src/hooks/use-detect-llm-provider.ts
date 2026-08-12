import { useState, useCallback } from "react";
import {
  detectProviderFromUrl,
  detectProviderAndModels,
} from "#/utils/detect-llm-provider";

interface ProviderDetectionState {
  isDetecting: boolean;
  detectedProvider: string | null;
  detectedModels: string[];
  confidence: "high" | "medium" | "low" | null;
  error: string | null;
}

export function useDetectLlmProvider() {
  const [state, setState] = useState<ProviderDetectionState>({
    isDetecting: false,
    detectedProvider: null,
    detectedModels: [],
    confidence: null,
    error: null,
  });

  const detectProvider = useCallback(
    async (baseUrl: string, apiKey?: string) => {
      if (!baseUrl) {
        setState({
          isDetecting: false,
          detectedProvider: null,
          detectedModels: [],
          confidence: null,
          error: null,
        });
        return;
      }

      setState((prev) => ({
        ...prev,
        isDetecting: true,
        error: null,
      }));

      try {
        const result = await detectProviderAndModels(baseUrl, apiKey);

        setState({
          isDetecting: false,
          detectedProvider: result.provider.displayName,
          detectedModels: result.models,
          confidence: result.provider.confidence,
          error: result.error || null,
        });
      } catch (error) {
        setState({
          isDetecting: false,
          detectedProvider: null,
          detectedModels: [],
          confidence: null,
          error: error instanceof Error ? error.message : "Detection failed",
        });
      }
    },
    [],
  );

  const detectProviderOnly = useCallback((baseUrl: string) => {
    if (!baseUrl) {
      setState({
        isDetecting: false,
        detectedProvider: null,
        detectedModels: [],
        confidence: null,
        error: null,
      });
      return null;
    }

    const result = detectProviderFromUrl(baseUrl);

    setState({
      isDetecting: false,
      detectedProvider: result.displayName,
      detectedModels: [],
      confidence: result.confidence,
      error: null,
    });

    return result;
  }, []);

  const reset = useCallback(() => {
    setState({
      isDetecting: false,
      detectedProvider: null,
      detectedModels: [],
      confidence: null,
      error: null,
    });
  }, []);

  return {
    ...state,
    detectProvider,
    detectProviderOnly,
    reset,
  };
}
