from ebooklib import epub

from bs4 import BeautifulSoup

from PIL import Image

import io
import os

import numpy as np

from Summarize import __read_epub_file__

def __get_indices__(bodylen, chapter_imgs):
    '''
    Calculates indices to evenly space out chapter images throughout the input chapter.

    Input:
        chapters_imgs - number of images to add to chapter
        bodylen - length of chapter body
    '''
    
    indices = list(np.linspace(1, bodylen-1, chapter_imgs)) # Calculate indices

    indices = [int(x.round()) for x in indices] # Round indices
    indices[0]=6 # Set first index to 6, so image doesn't appear at the top
    
    return indices


def __add_book_image__(book, imgname, path='imgs/'):
    '''
    Adds image to epub file image section

    Input:
        book - read epub file
        imgname - image file name
        path - image folder path
    '''
    
    img1 = Image.open(path+imgname) # Open image to img1 variable
    b = io.BytesIO()
    img1.save(b, 'jpeg')
    b_image1 = b.getvalue()
    
    # define Image file path in .epub
    image1_item = epub.EpubImage(uid=imgname, file_name='images/'+imgname, media_type='image/jpeg', content=b_image1)
    
    book.add_item(image1_item) # add image file to book

def __load_images__(path='imgs/', sort=True, verbose=False):
    '''
    Import image names from image folder to list and sorts them alphanumerically

    Input:
        path - image folder path
        verbose - if True prints list
    '''
    
    import os
    li = os.listdir('imgs/')

    if sort:
        li.sort()

    if verbose:
        print(li)
    
    return li

def create_book(summarized_book, original_epub_path, new_epub_name, chapter_indices, image_path='imgs/', verbose=True):

    book = __read_epub_file__(original_epub_path) # Read book file
    items = list(book.get_items()) # Get book items

    image_list = __load_images__(path=image_path) # Load all image names to list
    
    # Get number of summaries per chapter == the number of images to be added per chapter
    chapter_imgs = [len(x) for x in summarized_book.values()]


    j=-1 # Counter for loading images from folder

    for chapter_index in chapter_indices:
        chapter = items[chapter_index]
        
        soup = BeautifulSoup(chapter.content, 'html.parser') # Import chapter to soup
        number_chapter_imgs = chapter_imgs[chapter_index] # Retrieve number of images to add to chapter
        indices = __get_indices__(len(soup.html.body.section), number_chapter_imgs) # Calculate idices for images
        
        if verbose:
            print(indices)
    
        # Add images at indices to soup & add images to book
        for index in indices:
            j+=1 # Counter for loading images from folder
            
            new_tag = soup.new_tag('img', src='images/'+image_list[j]) # Create tag object
            soup.html.body.section.insert(index, new_tag) # Insert tag object to soup
            __add_book_image__(book, image_list[j], path=image_path) # Add image to book
    
        book.items[chapter_index].content = str.encode(str(soup)) # Replace book chapter with soup chapter
    
    epub.write_epub(new_epub_name, book, {}) # Write epub file to disk
    print('Finished!')