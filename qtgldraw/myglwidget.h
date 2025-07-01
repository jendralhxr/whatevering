#ifndef MYGLWIDGET_H
#define MYGLWIDGET_H

#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QElapsedTimer>
#include <QTimer>
#include <vector>

class MyGLWidget : public QOpenGLWidget, protected QOpenGLFunctions {
    Q_OBJECT
public:
    MyGLWidget(QWidget *parent = nullptr);
    ~MyGLWidget();

protected:
    void initializeGL() override;
    void paintGL() override;
    void resizeGL(int w, int h) override;

private:
    GLuint textureId = 0;
    int texWidth = 512;
    int texHeight = 512;
    std::vector<uchar> pixelData;

    void generateRandomPattern();

    // FPS tracking
    int frameCount = 0;
    QElapsedTimer fpsTimer;
    QTimer *fpsUpdateTimer = nullptr;
};

#endif // MYGLWIDGET_H
