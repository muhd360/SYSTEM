import fal_client

class VisionLanguageModel:
    def describe_image(self, image_url):
        result = fal_client.subscribe(
            "fal-ai/any-llm/vision",
            arguments={
                "model": "google/gemini-flash-1.5-8b",
                "prompt": "Describe this product image in detail, including any visible text, logos, or packaging information.",
                "system_prompt": "Provide a concise but detailed description of the product image.",
                "image_url": image_url,
            },
            with_logs=False,
        )
        return result.output

