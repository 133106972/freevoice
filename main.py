from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os
import uuid
import asyncio
from dotenv import load_dotenv
import edge_tts

# 加载环境变量
load_dotenv()

app = FastAPI(title="TTS Tool", description="文本转语音工具 - 基于 Edge TTS")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 音色配置 - Edge TTS 支持的语音
VOICE_OPTIONS = {
    "zh-CN-XiaoxiaoNeural": "晓晓 (女声)",
    "zh-CN-XiaoyiNeural": "晓伊 (女声)",
    "zh-CN-YunjianNeural": "云健 (男声)",
    "zh-CN-YunxiNeural": "云希 (男声)",
    "zh-CN-YunxiaNeural": "云夏 (男声)",
    "zh-CN-YunyangNeural": "云扬 (男声)",
    "zh-CN-liaoning-XiaobeiNeural": "晓北 (东北话女声)",
    "zh-CN-shaanxi-XiaoniNeural": "晓妮 (陕西话女声)",
    "zh-HK-HiuMaanNeural": "晓曼 (粤语女声)",
    "zh-HK-HiuGaaiNeural": "晓佳 (粤语女声)",
    "zh-HK-WanLungNeural": "云龙 (粤语男声)",
    "zh-TW-HsiaoChenNeural": "晓晨 (台湾话女声)",
    "zh-TW-YunJheNeural": "云哲 (台湾话男声)",
}

class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    speed: float = 1.0
    volume: float = 1.0

class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_url: str = None

def split_text(text: str, max_length: int = 3000) -> list:
    """将长文本分段"""
    if len(text) <= max_length:
        return [text]
    
    segments = []
    current = ""
    
    for char in text:
        if len(current) + 1 > max_length:
            segments.append(current)
            current = char
        else:
            current += char
    
    if current:
        segments.append(current)
    
    return segments

async def tts_single_segment(text: str, voice: str, speed: float, volume: float) -> bytes:
    """调用 Edge TTS 生成单段音频"""
    
    # Edge TTS 语速格式: 默认是 +0%，范围是 -100% 到 +100%
    # 我们的 speed 是 0.5-2.0，需要转换
    # speed 1.0 -> +0%
    # speed 0.5 -> -50%
    # speed 2.0 -> +100%
    rate = f"{int((speed - 1.0) * 100):+d}%"
    
    # Edge TTS 音量格式: 默认是 +0%，范围是 -100% 到 +100%
    volume_str = f"{int((volume - 1.0) * 100):+d}%"
    
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume_str
    )
    
    # 生成音频到内存
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return audio_data

@app.get("/", response_class=HTMLResponse)
async def root():
    """返回主页面"""
    return FileResponse("static/index.html")

@app.get("/api/voices")
async def get_voices():
    """获取可用音色列表"""
    return {"voices": VOICE_OPTIONS}

@app.post("/api/tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """生成 TTS 音频"""
    try:
        if not request.text.strip():
            return TTSResponse(success=False, message="文本不能为空")
        
        if request.voice not in VOICE_OPTIONS:
            return TTSResponse(success=False, message="无效的音色选择")
        
        # 分段处理
        segments = split_text(request.text)
        audio_parts = []
        
        for i, segment in enumerate(segments):
            try:
                audio_data = await tts_single_segment(
                    segment, 
                    request.voice, 
                    request.speed, 
                    request.volume
                )
                audio_parts.append(audio_data)
            except Exception as e:
                return TTSResponse(success=False, message=f"第 {i+1} 段生成失败: {str(e)}")
        
        # 合并音频
        combined_audio = b"".join(audio_parts)
        
        # 保存文件
        audio_id = str(uuid.uuid4())
        os.makedirs("static/temp", exist_ok=True)
        file_path = f"static/temp/{audio_id}.mp3"
        
        with open(file_path, "wb") as f:
            f.write(combined_audio)
        
        return TTSResponse(
            success=True,
            message="生成成功",
            audio_url=f"/static/temp/{audio_id}.mp3"
        )
        
    except Exception as e:
        return TTSResponse(success=False, message=f"生成失败: {str(e)}")

@app.delete("/api/cleanup")
async def cleanup():
    """清理临时文件"""
    try:
        temp_dir = "static/temp"
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
        return {"success": True, "message": "清理完成"}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8888))
    uvicorn.run(app, host="0.0.0.0", port=port)
