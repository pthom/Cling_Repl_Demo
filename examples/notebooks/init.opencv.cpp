#pragma cling add_library_path("/root/miniconda3/lib/")
#pragma cling add_include_path("/root/miniconda3/include")
// CONDA_DIR

#pragma cling load("libopencv_core.so")
#pragma cling load("libopencv_calib3d.so")
#pragma cling load("libopencv_highgui.so")
#pragma cling load("libopencv_imgcodecs.so")
#pragma cling load("libopencv_imgproc.so")

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "xtl/xbase64.hpp"
#include "nlohmann/json.hpp"

namespace im
{
    struct matshow
    {
        matshow(const cv::Mat& m) : _mat(m) {}
        cv::Mat _mat;
    };;
    matshow show(const cv::Mat& m) { matshow r(m); return r; }

    nlohmann::json mime_bundle_repr(const matshow& m)
    {
        std::vector<uchar> buf;
        bool success =  cv::imencode(".png", m._mat, buf);
        if (success) {
            auto bundle = nlohmann::json::object();
            std::string buf_as_str(buf.begin(), buf.end());
            bundle["image/jpeg"] = xtl::base64encode(buf_as_str);
            return bundle;
        }
        else
            return {};
    }
}
