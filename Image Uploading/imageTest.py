# https://www.tutorialspoint.com/how-to-compress-images-using-python-and-pil
# 9 September 2023 -- Compresses an image and then converts it to binary. Also converts from binary to an image.
# 4 October 2023 -- Binary conversion put on the backburner, focusing on uploading and compressing. 
# October 5 2023 -- Added bg removal

# import statements
from PIL import Image
import os 
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import numpy 
from rembg import remove
from colorthief import ColorThief
app = Flask(__name__)

# Color Codes
colorDict = {
    'black': ['000000', '0d140e', '222222'],
    'white' : ['ffffff'],
    'red' : ['ff0000', '7d1313'],
    'orange' : ['ffa500', '9c5708'],
    'yellow' : ['ffff00', 'e3e039'],
    'purple' : ['800080', 'ad23db'],
    'green' : ['008000', '335c22', '123d00'],
    'blue' : ['0000ff', '4079ff', '5e90ad', '033857', '2f355f'],
    'gray' : ['808080', '525252'],
    'pink' : ['ff7d94', '8f5b83'], 
    'brown' : ['964b00', '6b584f']
    }

# Keep track of upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the "binaries" directory if it doesn't exist
BINARIES_FOLDER = 'binaries'
#os.makedirs(BINARIES_FOLDER, exist_ok=True)

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Checks for allowed file extensions
# Parameters: The name of the file
# Returns: Boolean value on if the extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Corrected to match the HTML form
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Removes the background of the image
# Parameters: n -- file name
# Returns: Path to the background removed png
def removeBackground(n):
    #i = Image.open(n)
    new_n = compress(n)
    i = Image.open(new_n)
    out = remove(i)
    nsplit = n.split('.')
    n = nsplit[-2] + '_bg_rem.png'
    out.save(n)
    os.remove(new_n) # Remove the compressed version, only leaving the one with no bg
    return n

# Compresses images to half size, while optimizing
# PRE: Called by uploadImage
# Parameters: Image file name
# Returns: Path to the new compressed file
def compress(n):

    # Use PILLOW to open images
    i = Image.open(n)

    # Cut in half, add a filter to make it look cleaner
    i = i.resize((int(i.width/2),int(i.height/2)),Image.LANCZOS)

    # Get the directory and filename
    directory, filename = os.path.split(n)

    # Rename 
    new_n = os.path.join(directory, filename.rsplit('.', 1)[0] + '_comp.' + filename.rsplit('.', 1)[1])

    # Save optimized, 85% quality version
    i.save(new_n, optimize=True, quality=85)
    
    # Remove old file, keeping the compressed one
    os.remove(n)
    
    # Print the optimized size
    # i = Image.open(new_n) # Testing
    # print(i.size) # Testing
    return new_n # Returns the new file name

# Removes the background and returns the new file name/address
# Parameters: n -- Path to the image
# Returns: Path to the background removed image
def uploadImage(n):
    new_n = removeBackground(n)
    return new_n

# Get the main colors from the photo
# Parameters: name -- Name of the file to get the main color from
# Returns: The closest color in the color dictionary to the color
def getColor(name):
    colors = ColorThief(name)
    h = rgb2hex( colors.get_color(quality=1))
    print(h)
    return find_closest_color(h)
    #return h

# Convert RGB code to Hex
# Parameters: c -- rgb code to convert
# Returns the Hex code 
def rgb2hex(c):
    return "{:02x}{:02x}{:02x}".format(c[0],c[1],c[2])

# Finds the closest color in the color dictionary
# Parameters: Hex code for the image color
# Returns: The closest color in the dictionary to the Hex code
def find_closest_color(image_color):
    # Convert the image color to lowercase hex code
    image_color = image_color.lower()

    # Initialize variables to keep track of the closest color and difference
    closest_color = None
    min_difference = float('inf')

    # Iterate through the dictionary
    for color_name, hex_code in colorDict.items():
        for j in hex_code:
            # Calculate the color difference between the image color and the dictionary color
            difference = sum((int(image_color[i:i+2], 16) - int(j[i:i+2], 16))**2 for i in (0, 2, 4))

            # If the current difference is smaller than the minimum, update the closest color
            if difference < min_difference:
                closest_color = color_name
                min_difference = difference
        
    return closest_color

# Puts the correct template up
@app.route('/')
def index():
    return render_template('uploadTest.html')
    
# Uploads the photo from HTML
@app.route('/upload', methods=['POST'])
def upload_file():
    #print('upload call') # Testing
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']

    # If there is no file
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Upload file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_path)
        #new_n = compress(full_path) 
        new_n = uploadImage(full_path) # Doesn't remove background anymore
        
        category = request.form.get('category')
        if category == 'top':
            type = request.form.get('top_type')
            fit = request.form.get('top_fit')
            #color = request.form.get('top_color')
            pattern = request.form.get('top_pattern')
        elif category == 'bottom':
            type = request.form.get('bottom_type')
            fit = request.form.get('bottom_fit')
            #color = request.form.get('bottom_color')
            pattern = request.form.get('bottom_pattern')
        elif category == 'shoes':
            type = request.form.get('shoe_type')
            #color = request.form.get('shoe_color')
            pattern = request.form.get('shoe_pattern')
        #img = Image.open(new_n)
        
        # Trying to get main colors from picture
        color = getColor(new_n)
        #print(new_n)
        img = Image.open(new_n)
        #img.convert("RGB")
        img.show()
        #print(img.getcolors(img.size[0]*img.size[1]))
    
    if category == 'top' or category == 'bottom':
        return jsonify({'success': 'Upload success', 'image address': new_n, 'category': category, 'type': type, 
                        'fit': fit, 'color': color, 'pattern': pattern})
    if category == 'shoes':
        return jsonify({'success': 'Upload success', 'image address': new_n, 'category': category, 'type': type, 
                        'color': color, 'top pattern': pattern})
    else:
        return jsonify({'error': 'Invalid file format'})

# Runs the file
if __name__ == '__main__':
    app.run(debug=True)

# Testing
#uploadImage('test.jpg')


