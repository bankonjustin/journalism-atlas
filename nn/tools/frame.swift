// swift frame.swift in.mp4 out.png seconds   -> prints "duration WxH" and writes one frame
import Foundation
import AVFoundation
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let g = AVAssetImageGenerator(asset: asset); g.appliesPreferredTrackTransform = true
g.requestedTimeToleranceBefore = .zero; g.requestedTimeToleranceAfter = .zero
let img = try g.copyCGImage(at: CMTime(seconds: Double(a[3])!, preferredTimescale: 600), actualTime: nil)
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, img, nil); CGImageDestinationFinalize(d)
print(String(format: "duration %.2fs", CMTimeGetSeconds(asset.duration)), img.width, "x", img.height)
