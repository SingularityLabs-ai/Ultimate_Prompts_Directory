
# Google Veo Prompt Collection

(deprecated: have been merged with https://github.com/SingularityLabs-ai/Ultimate_Prompts_Directory)

Welcome to the **Google Veo Prompt Collection** repository! This repo contains a curated set of high-quality sample prompts for Google's Veo text-to-video model. Whether you're a creative, developer, or AI enthusiast, these prompts are designed to help you get started with Veo and inspire your own video generation projects.

---

## Table of Contents

- [About Google Veo](#about-google-veo)
- [Prompt Philosophy](#prompt-philosophy)
- [Prompt List](#prompt-list)
- [How to Use These Prompts](#how-to-use-these-prompts)
- [Prompt Engineering Tips](#prompt-engineering-tips)
- [Example API Usage](#example-api-usage)
- [Contributing](#contributing)
- [License](#license)

---

## About Google Veo

Google Veo is an advanced generative AI model capable of creating high-quality videos from natural language prompts. It supports a variety of styles, camera motions, and scene compositions, making it a powerful tool for both creative and professional use cases. Veo leverages deep learning to interpret detailed prompts and simulate realistic or stylized environments, characters, and actions[^4][^5][^6].

---

## Prompt Philosophy

Crafting effective prompts for Veo involves balancing creativity with clarity. A well-structured prompt typically includes:

- **Subject**: Who or what is the focus?
- **Context**: Where is the scene set?
- **Action**: What is happening?
- **Style**: Realistic, cinematic, cartoon, etc.
- **Camera Motion/Composition**: Wide shot, close-up, panning, etc.
- **Ambiance**: Lighting, mood, color palette.

The prompts in this repo demonstrate a range of genres, moods, and video techniques to showcase Veo’s versatility[^4].

---

## Prompt List

1. **Urban Sunrise**
*A wide-angle shot of a bustling city skyline at sunrise, golden light reflecting off skyscrapers, with birds flying overhead.*
2. **Rainy Street Noir**
*Cinematic close-up of a detective in a trench coat walking down a rain-soaked alley at night, neon lights reflecting on puddles.*
3. **Forest Time-lapse**
*Time-lapse of a dense forest as sunlight filters through the trees, shadows shifting and leaves rustling in the gentle breeze.*
4. **Futuristic Market**
*Sweeping drone shot of a vibrant, futuristic street market with holographic signs and diverse crowds in colorful attire.*
5. **Mountain Hiker**
*Medium shot of a hiker ascending a rocky mountain trail, mist swirling around, with dramatic clouds overhead.*
6. **Playful Puppy**
*Slow-motion close-up of a golden retriever puppy chasing a red ball across a grassy field on a sunny afternoon.*
7. **Space Dock Arrival**
*Wide shot of a spaceship docking at a massive orbital station, with astronauts floating nearby and Earth visible in the background.*
8. **Autumn Lake Reflection**
*Serene shot of a calm lake surrounded by autumn trees, their orange leaves mirrored perfectly in the water, with light ripples.*
9. **Jazz Club Vibes**
*Intimate, low-lit scene of a jazz quartet performing on stage in a smoky club, audience swaying to the rhythm, camera panning slowly.*
10. **Snowy Village Evening**
*Aerial shot of a cozy mountain village at dusk, snow falling gently, warm lights glowing from cottage windows, smoke rising from chimneys.*

---

## How to Use These Prompts

1. **Select a Prompt**: Choose any prompt from the list above that fits your creative goal.
2. **Input into Veo**: Paste the prompt into the Veo interface (Google Cloud Vertex AI Studio or via API).
3. **Adjust as Needed**: Customize the prompt by adding or modifying details (e.g., camera angle, lighting, style).
4. **Generate Video**: Run the prompt and review the generated video. Refine the prompt for improved results if necessary[^4][^5].

---

## Prompt Engineering Tips

- **Be Descriptive**: Use vivid adjectives and specific details to guide Veo’s output.
- **Set the Scene**: Specify context, ambiance, and style for richer results.
- **Incorporate Camera Directions**: Mention shot type, camera movement, and focus for cinematic effects.
- **Iterate**: Experiment with prompt variations to achieve your desired outcome.
- **Leverage Prompt Enhancement**: Veo’s prompt rewriter can automatically enrich your prompts for higher quality videos[^5].

---

## Example API Usage

Below is a Python example using the Google Gemini API to generate a video with Veo:

```python
import time
from google import genai
from google.genai import types

client = genai.Client()  # Reads API key from GOOGLE_API_KEY

operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt="Wide-angle shot of a bustling city skyline at sunrise, golden light reflecting off skyscrapers, with birds flying overhead.",
    config=types.GenerateVideosConfig(
        person_generation="dont_allow",
        aspect_ratio="16:9",
    ),
)

while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

for n, generated_video in enumerate(operation.response.generated_videos):
    client.files.download(file=generated_video.video)
    generated_video.video.save(f"video{n}.mp4")
```

For more code samples, see the [official Veo documentation][^6].

---

## Contributing

Contributions are welcome! Feel free to submit new prompts, suggest improvements, or open issues.

---

## License

This repository is released under the MIT License.

---

*Feel free to download this README.md as a markdown file for your own use or adaptation.*

---

**References:**

- [Vertex AI Video Generation Prompt Guide][^4]
- [Google Veo API Documentation][^6]
- [Veo | AI Video Generator][^5]

[^4]: https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide

[^5]: https://cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos

[^6]: https://ai.google.dev/gemini-api/docs/video

<div style="text-align: center">⁂</div>

[^1]: https://deepmind.google/models/veo/

[^2]: https://www.datacamp.com/tutorial/veo-3

[^3]: https://www.youtube.com/watch?v=Q2pR-Uz6PR8

[^4]: https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide

[^5]: https://cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos

[^6]: https://ai.google.dev/gemini-api/docs/video

[^7]: https://replicate.com/google/veo-2/examples

[^8]: https://nofilmschool.com/veo-3-examples

