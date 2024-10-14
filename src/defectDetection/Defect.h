#ifndef DEFECT_H
#define DEFECT_H

#include <opencv2/opencv.hpp>

class Defect {
private:
    int id;
    cv::Point2f center;
    double diameter;
    double area;

public:
    Defect(int _id, cv::Point2f _center, double _diameter, double _area)
        : id(_id), center(_center), diameter(_diameter), area(_area) {}

    int getId() const { return id; }
    cv::Point2f getCenter() const { return center; }
    double getDiameter() const { return diameter; }
    double getArea() const { return area; }

    void setCenter(cv::Point2f _center) { center = _center; }
    void setDiameter(double _diameter) { diameter = _diameter; }

    bool operator<(const Defect& other) const {
        return this->diameter > other.diameter;  // Sort in descending order of diameter
    }
};

#endif // DEFECT_H
