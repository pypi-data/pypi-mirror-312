#[allow(unused)]
#[macro_export]
macro_rules! measure_time {
    ($msg:expr, $block:block) => {{
        if cfg!(test) {
            let start = std::time::Instant::now();
            let result = { $block };
            println!("{} time taken: {:?}", $msg, start.elapsed());
            result
        } else {
            $block
        }
    }};
}

#[macro_export]
macro_rules! add_py_func {
    ($m: ident, $func:path) => {
        $m.add_function(wrap_pyfunction!($func, $m)?)?;
    };
}
