// swift mux.swift <video.mp4> <audio.m4a> <out.mp4>   (passthrough, faststart)
import AVFoundation
let a = CommandLine.arguments
let v = AVURLAsset(url: URL(fileURLWithPath: a[1])), au = AVURLAsset(url: URL(fileURLWithPath: a[2])), out = URL(fileURLWithPath: a[3])
try? FileManager.default.removeItem(at: out)
let comp = AVMutableComposition()
let vt = v.tracks.first { $0.mediaType == .video }!, at = au.tracks.first { $0.mediaType == .audio }!
let dur = v.duration
let ct = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try ct.insertTimeRange(CMTimeRange(start: .zero, duration: dur), of: vt, at: .zero)
let cta = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
try cta.insertTimeRange(CMTimeRange(start: .zero, duration: min(dur, au.duration)), of: at, at: .zero)
let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough)!
ex.outputURL = out; ex.outputFileType = .mp4; ex.shouldOptimizeForNetworkUse = true
let sem = DispatchSemaphore(value: 0); ex.exportAsynchronously { sem.signal() }; sem.wait()
print(ex.status == .completed ? "ok" : "failed: \(String(describing: ex.error))")
