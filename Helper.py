import numpy as np
import json
import copy

def __automatic_indices__(summarized_book, verbose=False):
    li = [len(x) for x in summarized_book.values()]

    indices_list = list()
    mean = np.mean(li)
    std = np.std(li)

    if verbose:
        print('mean, std')
        print(mean, std)

    
    for index, el in enumerate(li):
        if el > mean/2:
            indices_list.append(index)

    return indices_list
    

def get_chapter_indices(summarized_book, manual_first_index=None, manual_last_index=None):

    li = [len(x) for x in summarized_book.values()]
    print('Number of summaries made for each index:')
    print(li)

    bool_list = [bool(manual_first_index), bool(manual_last_index)]
    if sum(bool_list) == 1:
        raise Exception('Both indices need to be either both defined or both None')
    if sum(bool_list) == 2:
        return list(range(manual_first_index, manual_last_index+1))
    else:
        indices = __automatic_indices__(summarized_book)
        print('The following indices were identified as chapters:')
        print(indices)
        
        return indices

def make_scheduler_json(template_file, output_file, summarized_book, chapter_indices, checkpoint_name, cfg_scale=2, steps=5):
    '''
    Creates a JSON file that can be imported by sd-webui-agent-scheduler (https://github.com/ArtVentureX/sd-webui-agent-scheduler)

    Input:
        template_file: a JSON file containing a template for 1 prompt that is accepted by sd-webui-agent-scheduler
        output_file: path/name for output JSON file
        summarized_book: summarized book taken from summarize_ebook function
        chapter_indices: list of indices of chapters in summarized_book
    '''

    scheduler_json = list() # Initialize empty list
    
    # Create slice of summarized book values
    summarized_book_list_slice = list(list(summarized_book.values())[i] for i in chapter_indices)
    
    f = open(template_file) # Open template JSON file
    template = json.load(f)[0] # Load json template file
    
    for chapter in summarized_book_list_slice: # Iterate through elements of slice of summarized_book_list
        for part in chapter: # Iterate through summarized chapter parts   
            task = copy.deepcopy(template) # Make a deepcopy of the template JSON

            task['params']['checkpoint'] = checkpoint_name

            # Apply prompt to template
            task['params']['args']['prompt'] = part
            task['params']['args']['cfg_scale'] = cfg_scale
            task['params']['args']['steps'] = steps
            
            scheduler_json.append(task) # Add task to JSON

    # Write scheduler JSON to disk
    with open(output_file, 'w') as file:
        json.dump(scheduler_json, file)
