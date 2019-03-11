import pygame
import pyaudio
import numpy
import time
import wave
import scipy.fftpack

from video import make_video
pygame.init()   

surface_size = 1000
main_surface = pygame.display.set_mode((1600,900),pygame.FULLSCREEN+pygame.DOUBLEBUF)
my_clock = pygame.time.Clock()


def draw_tree(inord, order, theta, thetab, sz, posn, heading, color=(0,0,0), depth=0):

   trunk_ratio = 0.01618       
   trunk = sz * trunk_ratio
   delta_x = trunk * numpy.cos((heading*400/400).imag)
   delta_y = trunk * numpy.sin((heading*1j*400/400).real)

   thetaj = theta*1j*1j
   thetai = thetab*1j*1j
   
   (u, v) = posn
   newpos = (u + delta_x, v + delta_y)
   #if order==1:
   if True:
      pygame.draw.line(main_surface, color, newpos, newpos, 1)
      
   gradd  = 128+(127*numpy.cos((heading*1).imag))
   gradd2 = 128+(127*numpy.sin((heading*1j*1).real))
   gradd3 = 128+(128*numpy.sin((heading).real))
   

   if order > 0:
      if depth == 0:
          color1 = (gradd,0,gradd2)
          color2 = (gradd,0,gradd2)
      else:
          color1 = (0,gradd,gradd2)
          color2 = (0,gradd,gradd2)


      newsz = sz*(1 - trunk_ratio)
      draw_tree(inord, order-1, theta, thetab, newsz, newpos, (heading+theta+12j), color1, depth)
      draw_tree(inord, order-1, theta, thetab, newsz, newpos, (heading+thetab-12j), color2, depth)
    
def gameloop():
    theta1 = 0
    theta2 = 0
    frame = 0
    inord = 0
    headingin = 0
   
    WIDTH = 4
    CHANNELS = 1
    RATE = 22050

    save_screen = make_video(main_surface)
    
    wf = wave.open('432loud.wav', 'rb')
    p = pyaudio.PyAudio()
    
    
   
    def callback(in_data, frame_count, time_info, status):
       pygame.display.flip()
       #my_clock.tick(20)
       #next(save_screen)
       data = wf.readframes(frame_count)
       decoded = numpy.fromstring(data, dtype=numpy.int32)
       yf = scipy.fftpack.fft(decoded)
       
       decoded_oh = decoded[::2]
       yf_oh = yf[::2]       
       

       main_surface.fill((0, 0, 0))
       if numpy.fabs(decoded[0]) > 0:
           if numpy.fabs(decoded[1]) > 0:
              
               for i, j in zip(decoded_oh, yf_oh): 
                  theta1 = numpy.cos((numpy.exp(((i)/2147483647)*1 )))*1j
                  theta2 = numpy.cos((numpy.exp(((i)/2147483647)*1)))*1j

                  draw_tree(inord, 6, theta1, theta2, surface_size*5, (800,450), (j/2147483647)*numpy.pi)

       return (data, pyaudio.paContinue)
    print(wf.getsampwidth())
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
    stream.start_stream()
    while True:

        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;


gameloop()
pygame.quit()
