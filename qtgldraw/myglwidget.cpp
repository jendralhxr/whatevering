#include "myglwidget.h"
#include <QTimer>
#include <cstdlib>
#include <ctime>
#include <QDebug>

MyGLWidget::MyGLWidget(QWidget *parent)
    : QOpenGLWidget(parent)
{
    std::srand(std::time(nullptr));

    // Fast update timer
    QTimer *renderTimer = new QTimer(this);
    connect(renderTimer, &QTimer::timeout, this, QOverload<>::of(&MyGLWidget::update));
    renderTimer->start(0); // As fast as possible

    // FPS counter update every 1000 ms
    fpsTimer.start();
    fpsUpdateTimer = new QTimer(this);
    connect(fpsUpdateTimer, &QTimer::timeout, this, [=]() {
        qDebug() << "FPS:" << frameCount;
        frameCount = 0;
    });
    fpsUpdateTimer->start(1000); // 1-second interval
}

MyGLWidget::~MyGLWidget() {
    makeCurrent();
    if (textureId)
        glDeleteTextures(1, &textureId);
    doneCurrent();
}

void MyGLWidget::initializeGL() {
    initializeOpenGLFunctions();
    glEnable(GL_TEXTURE_2D);

    glGenTextures(1, &textureId);
    glBindTexture(GL_TEXTURE_2D, textureId);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    pixelData.resize(texWidth * texHeight * 3);
}

void MyGLWidget::generateRandomPattern() {
    for (int i = 0; i < pixelData.size(); ++i)
        pixelData[i] = static_cast<uchar>(std::rand() % 256);
}

void MyGLWidget::paintGL() {
    glClear(GL_COLOR_BUFFER_BIT);

    generateRandomPattern();

    glBindTexture(GL_TEXTURE_2D, textureId);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texWidth, texHeight, 0, GL_RGB, GL_UNSIGNED_BYTE, pixelData.data());

    glBegin(GL_QUADS);
    glTexCoord2f(0, 1); glVertex2f(-1.0f, -1.0f);
    glTexCoord2f(1, 1); glVertex2f( 1.0f, -1.0f);
    glTexCoord2f(1, 0); glVertex2f( 1.0f,  1.0f);
    glTexCoord2f(0, 0); glVertex2f(-1.0f,  1.0f);
    glEnd();

    frameCount++;  // Count frames
}

void MyGLWidget::resizeGL(int w, int h) {
    glViewport(0, 0, w, h);
}
