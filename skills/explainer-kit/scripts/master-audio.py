"""Master a narrated film's audio: voice to -16 LUFS / -1.5 dBTP, music bed sidechain-ducked under it.

usage (film root): <py> <skill>/scripts/master-audio.py --len 83.2 [--vo assets/audio/vo.mp3]
                   [--bed assets/audio/bgm-edit.wav] [--bed-gain -12] [--drops t1,t2 [--drop-len 0.25]]
Writes assets/audio/vo-master.wav and assets/audio/bgm-duck.wav and prints the loudness of each + the mix.
Why: one cloned-voice narration came in at -24 LUFS; a plain +8 dB lift clipped at +4.6 dBTP, loudnorm doesn't. The bed at
-12 dB + 5:1 sidechain sits ~17 dB under the voice and breathes up in the pauses. The final render measured -14.5 LUFS.
"""
import argparse, os, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--len", type=float, required=True)
ap.add_argument("--vo", default="assets/audio/vo.mp3")
ap.add_argument("--bed", default="assets/audio/bgm-edit.wav")
ap.add_argument("--bed-gain", type=float, default=-12)
# --drops 2.72,12.96 : the bed goes dead silent for --drop-len s right BEFORE each punch time, then hits back on it
# (the "silence drop" before a punch line).
ap.add_argument("--drops", default="")
ap.add_argument("--drop-len", type=float, default=0.25)
a = ap.parse_args()
DROPS = [float(x) for x in a.drops.split(",") if x.strip()]
# small frames first: volume eval=frame switches per frame, and the sidechain's big frames leaked a drop
gate = (",asetnsamples=n=256:p=0," + "volume='if(" + "+".join(f"between(t,{d - a.drop_len:.3f},{d - 0.01:.3f})" for d in DROPS)
        + ",0,1)':eval=frame") if DROPS else ""
VO, BED = "assets/audio/vo-master.wav", "assets/audio/bgm-duck.wav"
os.makedirs(".media", exist_ok=True)  # a fresh scaffold has no .media/ - ffmpeg failed on mix-check.wav

def ff(*x): subprocess.run(["ffmpeg", "-v", "error", "-y", *x], check=True)
def lufs(p):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i, pk = re.findall(r"I:\s+(-?[\d.]+) LUFS", o), re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)
    return f"{i[-1] if i else '?'} LUFS, peak {pk[-1] if pk else '?'} dBFS"

ff("-i", a.vo, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ar", "48000", VO)
if os.path.exists(a.bed):
    ff("-i", a.bed, "-i", VO, "-filter_complex",
       f"[0:a]aresample=48000,volume={a.bed_gain}dB[bed];[1:a]aresample=48000,apad[key];"
       f"[bed][key]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=400:makeup=1{gate}[o]",
       "-map", "[o]", "-t", str(a.len), "-ar", "48000", BED)
else:  # a film with no music: a silent bed keeps film.json's bgm track valid
    print(f"no bed at {a.bed} - writing a silent {BED}")
    ff("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(a.len), BED)
ff("-i", VO, "-i", BED, "-filter_complex", "amix=inputs=2:normalize=0", "-t", str(a.len), ".media/mix-check.wav")
print(f"voice {lufs(VO)} | bed {lufs(BED)} | mix {lufs('.media/mix-check.wav')}")
print('film.json: "audio": [{"id": "vo", "src": "assets/audio/vo-master.wav", ...}], "bgm": {"src": "assets/audio/bgm-duck.wav", "volume": 1}')
