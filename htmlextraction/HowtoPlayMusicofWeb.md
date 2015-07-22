##**< Web에 있는 음악을 Python에서 재생하기 >**  

####1. 개요  
Python코드에서 음악을 재생시키는데 음악의 소스가 인터넷인 경우의 방법.

####2. GStreamer  
(참고 링크 : http://yujuwon.tistory.com/94)
GStreamer는 리눅스 기반에서 streaming을 보다 쉽게 처리할 수 있도록 만든 open source framework이다.
Gstreamer를 이용하면 음원의 소스가 인터넷이든, 로컬이든 가능하다.

GStreamer를 이용하여 Web에 있는 음악을 재생하는 기본 코드는 아래와 같다.

	import pygst
	import gst

	def on_tag(bus, msg):
	    taglist = msg.parse_tag()
	    print 'on_tag:'
	    for key in taglist.keys():
	        print '\t%s = %s' % (key, taglist[key])

	#our stream to play
	music_stream_uri = 'http://www.samsunglions.com/upload/20140417151649.3480.6.0.mp3'

	#creates a playbin (plays media form an uri) 
	player = gst.element_factory_make("playbin", "player")

	#set the uri
	player.set_property('uri', music_stream_uri)

	#start playing
	player.set_state(gst.STATE_PLAYING)

	#listen for tags on the message bus; tag event might be called more than once
	bus = player.get_bus()
	bus.enable_sync_message_emission()
	bus.add_signal_watch()
	bus.connect('message::tag', on_tag)

	#wait and let the music play
	raw_input('Press enter to stop playing...')
    
