#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system(' pip install requests ffmpeg-python')
get_ipython().system(' pip install deepgram-sdk --upgrade')
get_ipython().system(' pip install requests')


# In[12]:


from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import requests

# Deepgram API key
DG_KEY = "25e6ee50ae75fd24e9f7d9b7453fe1cd883a9bbd" #hide later

# URL of the audio file
AUDIO_FILE = "student 001.mp3" #example audio

# Path to save the transcript json file
TRANSCRIPT_FILE = "transcript.json"
TRANSCRIPT_FILE_TXT = "transcript.txt"
def main():
    """Imports Audio File and Converts to Text"""
    """Outputs json and txt"""
    try:
        # STEP 1: Create a Deepgram client using the API key
        deepgram_client = DeepgramClient(DG_KEY)

        # Download the audio file from the URL
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=False, #punctuation and paragraph formatting disabled
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        output = deepgram_client.listen.rest.v("1").transcribe_file(payload, options)
        presentation=output['results']['channels'][0]['alternatives'][0]['transcript']
        
        # STEP 4: Write the response JSON to a file
        with open(TRANSCRIPT_FILE, "w") as transcript_file:
              transcript_file.write(output.to_json(indent=4))

        print("Transcript JSON file generated successfully.")
        # Optional STEP 5: Write the response TXT to a file
        with open(TRANSCRIPT_FILE_TXT,'w') as f:
              f.write(f"{presentation}\n")


        print("Transcript txt file generated successfully.")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()


# In[ ]:




