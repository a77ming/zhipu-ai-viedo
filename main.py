import logging
from flask import Flask, jsonify, request, send_from_directory
from zhipuai import ZhipuAI
import time

# 设置日志级别
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# 请填写您自己的APIKey
api_key = "6e6103db3ed970f9ef30d3ea5582dd40.ggCE9O29KxwGAiZF"  # 请替换为你的实际API Key
client = ZhipuAI(api_key=api_key)

def generate_video(prompt):
    try:
        response = client.videos.generations(
            model="cogvideox",
            prompt=prompt
        )
        logging.info("Video generation response: %s", response)
        return response.id
    except Exception as e:
        logging.error("Error generating video: %s", str(e))
        return None

def retrieve_video_result(video_id):
    while True:
        try:
            response = client.videos.retrieve_videos_result(
                id=video_id
            )
            logging.info("Video retrieval response: %s", response)
            if response.task_status == 'SUCCESS':
                return response.video_result
            elif response.task_status == 'FAILED':
                logging.error("Video generation failed: %s", response.error_message)
                return None
        except Exception as e:
            logging.error("Error retrieving video result: %s", str(e))
            return None
        time.sleep(10)

def video_results_to_dicts(video_results):
    return [
        {
            'url': video_result.url,
            'cover_image_url': video_result.cover_image_url
        }
        for video_result in video_results
    ]

@app.route('/generate-video', methods=['POST'])
def generate_video_route():
    data = request.json
    prompt = data.get('prompt', "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。")
    video_id = generate_video(prompt)
    if video_id:
        video_result = retrieve_video_result(video_id)
        if video_result:
            video_results_dict = video_results_to_dicts(video_result)
            return jsonify({
                'status': 'SUCCESS',
                'video_result': video_results_dict
            })
        else:
            return jsonify({
                'status': 'FAILED',
                'message': 'Failed to retrieve video result.'
            })
    else:
        return jsonify({
            'status': 'FAILED',
            'message': 'Failed to generate video.'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6067)