// H.264 MP4 from a PNG sequence with AVFoundation (no ffmpeg on this machine).
// swift encode.swift <frames_dir> <out.mp4> <width> <height> <fps> <bitrate_bps>
import Foundation
import AVFoundation
import CoreVideo
import ImageIO
import CoreGraphics
let a = CommandLine.arguments
let dir = a[1], out = a[2], W = Int(a[3])!, H = Int(a[4])!, fps = Int32(a[5])!, br = Int(a[6])!
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".png") }.sorted()
try? FileManager.default.removeItem(atPath: out)
let w = try AVAssetWriter(outputURL: URL(fileURLWithPath: out), fileType: .mp4)
w.shouldOptimizeForNetworkUse = true   // moov atom first (faststart)
let inp = AVAssetWriterInput(mediaType: .video, outputSettings: [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: W, AVVideoHeightKey: H,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: br, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoMaxKeyFrameIntervalKey: Int(fps) * 2, AVVideoExpectedSourceFrameRateKey: Int(fps)]])
let ad = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: inp, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA, kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H])
w.add(inp); w.startWriting(); w.startSession(atSourceTime: .zero)
for (i, f) in files.enumerated() {
  while !inp.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.002) }
  let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: dir + "/" + f) as CFURL, nil)!
  let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
  var pb: CVPixelBuffer?; CVPixelBufferPoolCreatePixelBuffer(nil, ad.pixelBufferPool!, &pb)
  CVPixelBufferLockBaseAddress(pb!, [])
  let ctx = CGContext(data: CVPixelBufferGetBaseAddress(pb!), width: W, height: H, bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(pb!), space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)!
  ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
  CVPixelBufferUnlockBaseAddress(pb!, [])
  ad.append(pb!, withPresentationTime: CMTime(value: Int64(i), timescale: fps))
}
inp.markAsFinished()
let sem = DispatchSemaphore(value: 0); w.finishWriting { sem.signal() }; sem.wait()
print(w.status == .completed ? "ok \(files.count) frames" : "failed: \(String(describing: w.error))")
