// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "AppleSpriteKitConformance",
    platforms: [.macOS(.v15), .iOS(.v17), .tvOS(.v17), .visionOS(.v1)],
    products: [
        .library(name: "ConformanceCore", targets: ["ConformanceCore"]),
        .executable(name: "AppleSpriteKitDemo", targets: ["AppleSpriteKitDemo"])
    ],
    targets: [
        .target(name: "ConformanceCore"),
        .executableTarget(
            name: "AppleSpriteKitDemo",
            dependencies: ["ConformanceCore"]
        ),
        .testTarget(
            name: "ConformanceCoreTests",
            dependencies: ["ConformanceCore"]
        )
    ]
)
