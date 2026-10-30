// swift silence.swift <out.m4a> <seconds>
import AVFoundation
let a = CommandLine.arguments; let out = URL(fileURLWithPath: a[1]); let secs = Double(a[2])!
try? FileManager.default.removeItem(at: out)
let fmt = AVAudioFormat(standardFormatWithSampleRate: 44100, channels: 2)!
var f: AVAudioFile? = try AVAudioFile(forWriting: out, settings: [AVFormatIDKey: kAudioFormatMPEG4AAC, AVSampleRateKey: 44100, AVNumberOfChannelsKey: 2, AVEncoderBitRateKey: 64000])
var left = Int(secs * 44100)
while left > 0 { let n = min(left, 4096); let b = AVAudioPCMBuffer(pcmFormat: fmt, frameCapacity: AVAudioFrameCount(n))!; b.frameLength = AVAudioFrameCount(n)
  for c in 0..<2 { memset(b.floatChannelData![c], 0, n * 4) }; try f!.write(from: b); left -= n }
f = nil
print("ok")
