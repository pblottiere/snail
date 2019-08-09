import QtQuick 2.0
import QtCharts 2.0

ChartView {
    anchors.fill: parent
    objectName: "view"
    antialiasing: true
    legend.visible: false
    backgroundColor: snail.background_color
    margins.left: 0
    margins.right: 0
    margins.top: 0
    margins.bottom: 0
    height: 400

    LineSeries {
        id: cpu_series
        color: snail.cpu_color
        width: 2
        objectName: "series"
        name: "series_name"
        axisX: axisX
        axisY: axisY
    }

    ValueAxis {
        objectName: "axeX"
        id: axisX
        min: 0
        max: snail.max
        color: snail.axis_color
        labelsColor: snail.axis_color
        gridLineColor: snail.axis_color
        minorGridLineColor: snail.axis_color
        shadesColor: snail.axis_color
        shadesBorderColor: snail.axis_color
        visible: true
        minorGridVisible: false
        gridVisible: false
        labelsVisible: false
        lineVisible: true
        shadesVisible: false
    }

    ValueAxis {
        objectName: "axeY"
        id: axisY
        min: 0
        max: 100
        color: snail.axis_color
        labelsColor: snail.axis_color
        gridLineColor: snail.axis_color
        minorGridLineColor: snail.axis_color
        shadesColor: snail.axis_color
        shadesBorderColor: snail.axis_color
        visible: true
        minorGridVisible: false
        gridVisible: false
        labelsVisible: true
        lineVisible: true
        shadesVisible: false
    }

    Component.onCompleted: {
        snail.set_series_id(cpu_series)
    }
}
