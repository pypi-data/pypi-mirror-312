extern crate prost_build;

fn main() {
    let protoc_path = match std::env::var("PROTOC") {
        Ok(path) if !path.is_empty() => std::path::PathBuf::from(path),
        _ => protoc_bin_vendored::protoc_bin_path().expect("protoc is not available"),
    };
    println!(
        "use protoc {} to generate pb files",
        protoc_path.to_str().unwrap()
    );
    std::env::set_var("PROTOC", protoc_path);
    let mut config = prost_build::Config::new();
    config.bytes(&["."]);
    config
        .compile_protos(&["src/logs.proto"], &["src/"])
        .unwrap();
    // prost_build::compile_protos(&["src/logs.proto"], &["src/"]).unwrap();
}
