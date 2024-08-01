import streamlit as st
import cv2
import numpy as np
import moviepy.editor as mp
import os

def get_video_dimensions(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error opening video file")
        return None, None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height

def resize_video(video_path, target_aspect_ratio, output_path):
    clip = mp.VideoFileClip(video_path)
    current_aspect_ratio = clip.w / clip.h
    if np.isclose(current_aspect_ratio, target_aspect_ratio, atol=0.01):
        st.warning("The video already has the desired aspect ratio.")
        clip.write_videofile(output_path, codec='libx264')
        return True
    elif current_aspect_ratio > target_aspect_ratio:
        # Crop width
        new_width = int(clip.h * target_aspect_ratio)
        crop_width = (clip.w - new_width) / 2
        clip = clip.crop(x1=crop_width, x2=clip.w - crop_width)
    else:
        # Crop height
        new_height = int(clip.w / target_aspect_ratio)
        crop_height = (clip.h - new_height) / 2
        clip = clip.crop(y1=crop_height, y2=clip.h - crop_height)
    
    clip.write_videofile(output_path, codec='libx264')
    return True

def main():
    st.title("Video Aspect Ratio Modifier")
    
    uploaded_files = st.file_uploader("Upload three video files", type=["mp4", "avi", "mov", "mkv"], accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) == 3:
        aspect_ratio = st.text_input("Enter the desired aspect ratio (e.g., 16:9 or 4:3):")
        
        if aspect_ratio:
            try:
                ar_width, ar_height = map(int, aspect_ratio.split(':'))
                target_aspect_ratio = ar_width / ar_height
            except ValueError:
                st.error("Invalid aspect ratio format. Please use the format 'width:height' (e.g., 16:9).")
                return
            
            for i, uploaded_file in enumerate(uploaded_files):
                video_path = f"temp_video_{i}.mp4"
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                width, height = get_video_dimensions(video_path)
                
                if width is not None and height is not None:
                    st.write(f"Original video {i+1} dimensions: {width} x {height}")
                    
                    output_path = f"output_video_{i}.mp4"
                    if resize_video(video_path, target_aspect_ratio, output_path):
                        st.success(f"Video {i+1} has been successfully modified.")
                        st.video(output_path)
                    else:
                        st.error(f"Video {i+1} aspect ratio modification failed.")
    else:
        st.info("Please upload exactly three video files.")
    
if __name__ == "__main__":
    main()
