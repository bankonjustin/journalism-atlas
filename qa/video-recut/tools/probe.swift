import AVFoundation
let a = CommandLine.arguments; let u = AVURLAsset(url: URL(fileURLWithPath: a[1]))
print("duration", CMTimeGetSeconds(u.duration))
for t in u.tracks { let d = (t.formatDescriptions as! [CMFormatDescription])[0]
  print(t.mediaType.rawValue, CMFormatDescriptionGetMediaSubType(d).description, "fps", t.nominalFrameRate, "size", t.naturalSize, "kbps", Int(t.estimatedDataRate/1000))
  if t.mediaType == .video, let ex = CMFormatDescriptionGetExtensions(d) as? [String: Any], let atoms = ex["SampleDescriptionExtensionAtoms"] as? [String: Any], let avcc = atoms["avcC"] as? Data { print("avcC profile_idc", avcc[1], "(100=High)", "level_idc", avcc[3]) } }
