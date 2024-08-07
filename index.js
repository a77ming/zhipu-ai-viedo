const generateBtn = document.getElementById('generateBtn');
const promptInput = document.getElementById('promptInput');
const loading = document.getElementById('loading');
const videoSection = document.getElementById('videoSection');
const videoCover = document.getElementById('videoCover');
const videoLink = document.getElementById('videoLink');

generateBtn.addEventListener('click', function() {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        alert('请输入你的提示词');
        return;
    }

    if (generateBtn.disabled) {
        alert('视频生成中，请稍后...');
        return;
    }

    generateBtn.disabled = true;
    loading.style.display = 'block';
    videoSection.style.display = 'none';

    fetch('/generate-video', {  // 这里使用相对路径
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'SUCCESS') {
            videoCover.src = data.video_result[0].cover_image_url;
            videoLink.href = data.video_result[0].url;
            videoSection.style.display = 'block';
        } else {
            alert('视频生成失败，请重试');
        }
    })
    .catch(error => {
        console.error('错误:', error);
        alert('视频生成失败，请重试');
    })
    .finally(() => {
        loading.style.display = 'none';
        generateBtn.disabled = false;
    });
});