#include <QApplication>
#include <QMainWindow>
#include "myglwidget.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    QMainWindow window;

    MyGLWidget *glWidget = new MyGLWidget();
    window.setCentralWidget(glWidget);
    window.resize(800, 600);
    window.show();

    return app.exec();
}
