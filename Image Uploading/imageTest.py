# https://www.tutorialspoint.com/how-to-compress-images-using-python-and-pil

# import statements
from PIL import Image

# Compresses images to half size, while optimizing
# PRE: Called by uploadImage
# Parameters: Image file name
def compress(n):

    # Use PILLOW to open images
    i = Image.open(n)

    # Print regular size
    # print(i.size) # Testing

    # Cut in half, add a filter to make it look cleaner
    i = i.resize((int(i.width/2),int(i.height/2)),Image.LANCZOS)

    # Save optimized, 85% quality version
    i.save('resized_test.jpg', optimize=True, quality=85)
    
    # Print the optimized size
    #i = Image.open('resized_test.jpg') # Testing
    #print(i) # Testing

# Converts to binary to be able to store in database
# PRE: Called by uploadImage
# Parameters: Image file name
def convertToBinary(n):
    with open(n, 'rb') as file:
        binaryData = file.read()
    return binaryData

# Uploads image
# Parameters: n -- file name to upload
def uploadImage(n):
    compress(n)
    convertToBinary(n)

# Write binary data to a new file
# Parameters: Data -- binary data, n -- new file name
def writeToImage(data, n):
    with open(n, 'wb') as file:
        file.write(data)

# Testing
# uploadImage('testImage.jpg')
# writeFile(convertToBinary('testImage.jpg'), 'output.jpg')


