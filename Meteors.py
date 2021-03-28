from PIL import Image
import PIL
import time

#function to find surface borders of the lakes
def water_finder(img, water, i, j):
    water_qtt = i
    lake = [0]*2
    lake[0] = i
    already_found = 1
    #check if lake have been already found
    if(water):
        for lakes in water:
            if(i<lakes[0] or i>lakes[1]):
                already_found = 0
            else:
                already_found = 1
                break;
    else:
        already_found = 0

    while(img.getpixel((i,j)) == (0, 0, 255, 255)):
        i+=1
    #adding the new lake borders
    if(already_found == 0):
        lake[1]=i-1
        water.append(lake)
    else:
        pass
    water_qtt = i - water_qtt
    return (i, water_qtt)

#function to get meteors that will fall on the water
def water_meteors(meteors_pos, water):
    perpendicular_meteor = 0
    perpendicular_meteor_pos = []
    for m in meteors_pos:
        for w in water:
            if(m[0] >= w[0] and m[0] <= w[1]): #meteors in water limits
                perpendicular_meteor+=1
                perpendicular_meteor_pos.append(m)
            else:
                pass
    return(perpendicular_meteor, perpendicular_meteor_pos)

def bin_to_asc(binaries):
    str=''
    for b in binaries:
        if(int(b,2)>32 and int(b,2)<126):
            str+=(chr(int(b,2)))
    print(str)
    #print(len(str))

def img_to_bin2(img, sky_dots_pos, perpendicular_meteor_pos, height, width):
    str_temp='0'
    binaries=[]
    for j in range (0, 399):
        i=0
        while (i < width):
            img_color_temp = img.getpixel((i,j))
            for p in img_color_temp[:-1]:
                if (len(str_temp)==7):
                    str_temp+='0'
                if (len(str_temp)==8):
                    if (str_temp != '00000000' and str_temp != '11111111'):
                        binaries.append(str_temp)
                    str_temp='0'
                if (p==255 or p==0):
                    str_temp+='1'
                else:
                    str_temp+='0'
                i+=1
    #print(binaries)
    bin_to_asc(binaries)

def img_to_bin(img, sky_dots_pos, perpendicular_meteor_pos):
    binaries=[]
    bin_str=''
    print('\n')
    #print(len(sky_dots_pos))
    #print(len(perpendicular_meteor_pos))

    # 255->1 and 0->0 removing perpendicular meteors
    str_temp=''
    for s in sky_dots_pos:
        img_color_temp = img.getpixel((s[0],s[1]))
        for p in img_color_temp[:-1]:
            if (len(str_temp)==7):
                str_temp+=''
            if (len(str_temp)==8):
                binaries.append(str_temp)
                str_temp=''
            if (p==255):
                str_temp+='1'
            elif (p==0):
                str_temp+='0'
    str_temp = str_temp + '0'*(8-len(str_temp))
    binaries.append(str_temp)
    print('with'+str(len(binaries)))
    #print(binaries, end= '\n')
    bin_to_asc(binaries)
    k=0
    binaries=[]
    bin_str=''
    for s in sky_dots_pos:
        water_meteor = 0
        img_color_temp = img.getpixel((s[0],s[1]))
        for pm in perpendicular_meteor_pos:
            if ([s[0],s[1]] == pm):
                water_meteor = 1
        if(water_meteor == 0):
            for p in img_color_temp[:-1]:
                if (len(str_temp)==7):
                    str_temp+=''
                if (len(str_temp)==8):
                    binaries.append(str_temp)
                    str_temp=''
                if (p==255):
                    str_temp+='1'
                elif (p==0):
                    str_temp+='0'
        else:
            pass
    str_temp = str_temp + '0'*(8-len(str_temp))
    binaries.append(str_temp)
    print('without'+str(len(binaries)))
    #print(binaries, end= '\n')
    bin_to_asc(binaries)

#only perpendicular meteors
def img_to_bin3(img, sky_dots_pos, perpendicular_meteor_pos):
    binaries=[]
    bin_str=''
    print('\n')
    #print(len(sky_dots_pos))
    #print(len(perpendicular_meteor_pos))

    # 255->1 and 0->0 removing perpendicular meteors
    str_temp=''
    for s in sky_dots_pos:
        water_meteor = 0
        img_color_temp = img.getpixel((s[0],s[1]))
        if(img_color_temp == (255,255,255,255)):
            for p in img_color_temp[:-1]:
                if (len(str_temp)==7):
                    str_temp+=''
                if (len(str_temp)==8):
                    binaries.append(str_temp)
                    str_temp=''
                if (p==255):
                    str_temp+='0'
                elif (p==0):
                    str_temp+='1'
        else:
            for pm in perpendicular_meteor_pos:
                if ([s[0],s[1]] == pm):
                    water_meteor = 1
            if(water_meteor == 1):
                for p in img_color_temp[:-1]:
                    if (len(str_temp)==7):
                        str_temp+=''
                    if (len(str_temp)==8):
                        binaries.append(str_temp)
                        str_temp=''
                    if (p==255):
                        str_temp+='1'
                    elif (p==0):
                        str_temp+='0'
            else:
                pass
    str_temp = str_temp + '0'*(8-len(str_temp))
    binaries.append(str_temp)
    print('without'+str(len(binaries)))
    #print(binaries, end= '\n')
    bin_to_asc(binaries)

def main():

    filename = "meteor_challenge_01.png" #path
    img = Image.open(filename)

    #-- counting color pixels --#
    width, height = img.size
    water = [] #stores "lakes" limits
    colors_qtd = [0]*4 #stores the 4 pure colors
    meteors_pos = []
    stars_pos = []
    sky_dots_pos =[]
    lowest_in_sky = 0
    i=0
    for j in range (0, height):
        i=0
        while (i < width):
            img_pixel = img.getpixel((i,j))
            #white
            if (img_pixel[0] == img_pixel[1] and img_pixel[1] == img_pixel[2] and img_pixel[2] == 255):
                colors_qtd[0] += 1
                stars_pos.append([i,j])
                lowest_in_sky = j
                sky_dots_pos.append([i,j])
            #black
            elif (img_pixel[0] == img_pixel[1] and img_pixel[1] == img_pixel[2] and img_pixel[2] == 0):
                colors_qtd[1] += 1
            #red
            elif (img_pixel[0] == 255 and img_pixel[1] == img_pixel[2] and img_pixel[2] == 0):
                colors_qtd[2] += 1
                lowest_in_sky = j
                meteors_pos.append([i,j])   #position x,y of all meteors
                sky_dots_pos.append([i,j])
            #blue
            elif(img_pixel[2] == 255 and img_pixel[0] == img_pixel[1] and img_pixel[1] == 0):
                r = water_finder(img, water, i, j)
                i = r[0]
                i=i-1
                colors_qtd[3] += r[1]
            else:
                pass
                #print(img_pixel)
            i+=1

    p_meteor_res = water_meteors(meteors_pos, water)
    perpendicular_meteor = p_meteor_res[0]
    perpendicular_meteor_pos = p_meteor_res[1]

    #img_to_bin(img, sky_dots_pos, perpendicular_meteor_pos)

    amount=0
    sky_dots_pos = []
    for i in range (0,width):
        for j in range (0,lowest_in_sky+1):
            img_pixel = img.getpixel((i,j))
            #white
            if (img_pixel[0] == img_pixel[1] and img_pixel[1] == img_pixel[2] and img_pixel[2] == 255):
                sky_dots_pos.append([i,j])
            #red
            elif (img_pixel[0] == 255 and img_pixel[1] == img_pixel[2] and img_pixel[2] == 0):
                sky_dots_pos.append([i,j])
            else:
                pass
                #print(img_pixel)
            amount+=1
    #img_to_bin(img, sky_dots_pos, perpendicular_meteor_pos)

    #img_to_bin3(img, sky_dots_pos, perpendicular_meteor_pos)


    print(' ')

    # -- Printing results -- #
    print('Lakes borders', end=' ') #surface borders of the lakes
    print(water)

    str_temp = ["Stars", "Ground", "Meteors", "Water"]
    for i in range (len(colors_qtd)):
        print(str_temp[i], end = ' ')
        print(str(colors_qtd[i]))




    print('Perpendicular meteors', end = ' ')
    print(perpendicular_meteor)
    print()

    del img

if (__name__ == '__main__'):
    time1 = time.time()
    main()
    print("\n--- %s seconds ---" % (time.time() - time1))
