import requests

with open('cid', 'r') as cfile:
    client_id = cfile.read()
# Replace with your Imgur API client ID


def upload_image_to_imgur(image_path): 
    # Prepare headers for the Imgur API request
    headers = {'Authorization': f'Client-ID {client_id}'}

    # Create a dictionary for the data you want to send (image)
    files = {'image': open(image_path, 'rb')}

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
    image_path = "C:\\Users\\adird\\newfuckingfoldeer\\coverPhoto.jpg"
    uploaded_url = upload_image_to_imgur(image_path)

    if uploaded_url:
        print("Image successfully uploaded to Imgur. Link:", uploaded_url)
    else:
        print("Image upload to Imgur failed.")
