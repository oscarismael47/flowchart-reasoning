from groq import Groq
import base64
import os
import streamlit as st

API_KEY = st.secrets.get("GROQ_KEY")

GROQ_MODEL_VISION = st.secrets.get("GROQ_MODEL_VISION")


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_groq(image_path, prompt="What's in this image?"):
    """
    Sends an image and prompt to the Groq vision model and returns the response.

    Args:
        image_path (str): Path to the image file.
        prompt (str): The prompt/question for the model.

    Returns:
        str: The model's response.
    """
    base64_image = encode_image(image_path)
    client = Groq(api_key=API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model=GROQ_MODEL_VISION,
    )
    return chat_completion.choices[0].message.content


# Path to your image
#image_path = "puml_examples/flow_1_crop_1.png"
#result = analyze_image_with_groq("puml_examples/flow_1_crop_1.png", "Describe the flowchart in this image.")
#print(result)


d = """
The diagram models the process of handling a member's shopping cart and coupon application in an e-commerce system. Here's how it works step-by-step:

It starts by retrieving the shopping cart information, calculating any initial discounts, and fetching the member's shipping addresses and all their coupons.

Then, for each coupon, the system checks whether the coupon is usable based on its type:

If it is a universal coupon, it checks if the total amount in the cart meets the coupon's minimum required threshold. If yes, the coupon is added to the available list; otherwise, it is added to the unavailable list.
If not universal, it checks if it is category-specific. If so, it verifies if the total amount in that category meets the minimum threshold.
If not category-specific, it checks if it is product-specific, verifying if the total amount of the specific products meets the threshold.
If the coupon does not fit any of these types or fails the checks, it is marked unavailable or no coupons are available.
This process repeats until all coupons are evaluated.

After processing all coupons, the system retrieves the member's available coupons, their points balance, and the rules for using points.

Finally, it calculates the total amount payable by incorporating the total purchase amount, activity promotions, coupons applied, and points used.

The process ends with this final calculation.

In essence, the flow determines which coupons a user can use and applies all discounts and point redemptions to calculate the final payment.
"""