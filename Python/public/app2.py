import asyncio
from CPUdata import CPUdata
import logging
import websockets
import datetime
import json
import os
from DSText2 import Audio, VADAudio
import argparse
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send("Pong")
DEFAULT_SAMPLE_RATE = 16000

parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                    help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
parser.add_argument('--nospinner', action='store_true',
                    help="Disable spinner")
parser.add_argument('-w', '--savewav',
                    help="Save .wav files of utterences to given directory")
parser.add_argument('-f', '--file',
                    help="Read from .wav file instead of microphone")

parser.add_argument('-m', '--model', required=True,
                    help="Path to the model (protocol buffer binary file, or entire directory containing all standard-named files for model)")
parser.add_argument('-s', '--scorer',
                    help="Path to the external scorer file.")
parser.add_argument('-d', '--device', type=int, default=None,
                    help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
parser.add_argument('-r', '--rate', type=int, default=DEFAULT_SAMPLE_RATE,
                    help=f"Input device sample rate. Default: {DEFAULT_SAMPLE_RATE}. Your device may require 44100.")

ARGS = parser.parse_args()
if ARGS.savewav: os.makedirs(ARGS.savewav, exist_ok=True)

async def wsJson(websocket):
    while True:
        CpuData = CPUdata.getJsonData(CPUdata)
        
        #await websocket.send(json.dumps(CpuData, default=str))
        if os.path.isdir(ARGS.model):
            model_dir = ARGS.model
            ARGS.model = os.path.join(model_dir, 'output_graph.pb')
            ARGS.scorer = os.path.join(model_dir, ARGS.scorer)

        print('Initializing model...')
        logging.info("ARGS.model: %s", ARGS.model)
        model = deepspeech.Model(ARGS.model)
        if ARGS.scorer:
            logging.info("ARGS.scorer: %s", ARGS.scorer)
            model.enableExternalScorer(ARGS.scorer)

        # Start audio with VAD
        vad_audio = VADAudio(aggressiveness=ARGS.vad_aggressiveness,
                            device=ARGS.device,
                            input_rate=ARGS.rate,
                            file=ARGS.file)
        print("Listening (ctrl-C to exit)...")
        frames = vad_audio.vad_collector()

        # Stream from microphone to DeepSpeech using VAD
        spinner = None
        if not ARGS.nospinner:
            spinner = Halo(spinner='line')
        stream_context = model.createStream()
        wav_data = bytearray()
        for frame in frames:
            if frame is not None:
                if spinner: spinner.start()
                logging.debug("streaming frame")
                stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
                if ARGS.savewav: wav_data.extend(frame)
            else:
                if spinner: spinner.stop()
                logging.debug("end utterence")
                if ARGS.savewav:
                    vad_audio.write_wav(os.path.join(ARGS.savewav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav")), wav_data)
                    wav_data = bytearray()
                text = stream_context.finishStream()
                #send text to websocket here
                await websocket.send(text)
                print("Recognized: %s" % text)
                stream_context = model.createStream()

        await asyncio.sleep(1)


async def main():
    async with websockets.serve(wsJson, "192.168.3.211", 5000):
        await asyncio.Future()  # run forever

asyncio.run(main())