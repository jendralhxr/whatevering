        for c in countours:
            hull = cv2.convexHull(c)
            draw = cv2.drawContours(image_convert_Towhite, [hull], 0, (0, 255, 0), thickness=2)  # cv2.filled
            cv2.imshow('Contours', draw)
            if cv2.contourArea(c) < 500:
                continue
            draw2 = cv2.drawContours(image1, [hull], -1, (255, 255, 0), thickness=2)
            draw2 = cv2.drawContours(image_convert_Towhite, [hull], -1, (0, 255, 255), thickness=2)
            cv2.imshow('Lokal Segement', draw2)
            (x_b, y_b, w_b, h_b) = cv2.boundingRect(c)
            cv2.rectangle(image1, (x_b, y_b), (x_b + w_b, y_b + h_b), (255, 255, 0), 2)
            roi_save=image1[y_b:y_b+h_b, x_b:x_b+w_b]
            # cv2.imwrite('roi_1.jpg',roi_save)
            save=0
            while (len(c)>0):
                cv2.imwrite('output_roi/' + 'roi_' + str([save]) + '.png',roi_save)
                save=save+1