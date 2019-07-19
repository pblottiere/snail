import QtQuick 2.0
import QtCharts 2.0

ChartView {
    anchors.fill: parent
    objectName: "view"
    antialiasing: true
    legend.visible: false
    margins.left: 0
    margins.right: 0
    margins.top: 0
    margins.bottom: 0
    height: 400

    LineSeries {
        id: series_id
        objectName: "series"
        name: "series_name"
        axisX: axisX
        axisY: axisY
    }

    ValueAxis {
        objectName: "axeY"
        id: axisX
        visible: false
        min: 0
        max: snail.max
    }

    ValueAxis {
        objectName: "axeX"
        id: axisY
        min: 0
        max: 100
    }

    Component.onCompleted: {
        snail.set_series_id(series_id)
    }

    // Timer {
    //     interval: 100
    //     running: true
    //     repeat: false
    //     onTriggered: snail.setSeriesId(series_id)

    //     // onTriggered: {
    //     //     worker.sendMessage();
    //     // }
    // }

    // WorkerScript {
    //     id: worker

    //     onMessage: {
    //         snail.update(series_id)
    //         // series_id.append(0, 25)
    //         // series_id.append(1, 50)
    //         // series_id.append(2, 75)
    //     }
    // }
}
