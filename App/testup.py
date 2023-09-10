import requests

# Replace with your Imgur API client ID
client_id = "275b95ebffdeabc"

def upload_image_to_imgur(image_data): 
    # Prepare headers for the Imgur API request
    headers = {'Authorization': f'Client-ID {client_id}'}

    # Create a dictionary for the data you want to send (image)
    files = {'image': image_data}

    # Send the image to Imgur API
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)

    if response.status_code == 200:
        # Successfully uploaded the image
        imgur_response = response.json()
        img_url = imgur_response['data']['link']
        return img_url
    else:
        # Failed to upload the image
        print("Image upload failed. Status code:", response.status_code)
        return None

if __name__ == "__main__":
    # Example: You should pass the image data from your frontend to this function.
    # Replace 'image_data_from_frontend' with the actual image data you receive.
    image_data_from_frontend = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'

    uploaded_url = upload_image_to_imgur(image_data_from_frontend)

    if uploaded_url:
        print("Image successfully uploaded to Imgur. Link:", uploaded_url)
    else:
        print("Image upload to Imgur failed.")
