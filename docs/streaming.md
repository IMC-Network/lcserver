# Streaming using IMC LiveCloud Server
Setting up a server for RTMP to HLS streaming is straightforward. The process
only requires a few commands which can be configured to the operator's liking,
allowing for multiple streams to be remuxed at once.

To start streaming, launch IMC LiveCloud Server. Then, enter in the following
commands:

```
new Streamer stream
do stream useConfigurationTemplate specifyParameters
```

You'll now be prompted to enter certain parameters which will affect the way
streaming works. Values must be entered on a line-by-line basis, and in the
format `key: value`:

```
rtmpPort: 1935
rtmpStreamName: live
hlsStreamPath: /
```

The `rtmpPort` parameter is the port on which the RTMP stream should be streamed
into. The `rtmpStreamName` determines the name of the stream path to use.
Finally, the `hlsStreamPath` is the path at which others can view your stream.

After pressing the Enter key once more, the configuration will be saved. Next,
to run the streamer, type:

```
do stream start
```

Now, you can start streaming from your favourite streaming software. For the
purposes of this demonstration, you should configure your streaming software to
stream to `rtmp://localhost:1935/live/` and with the streaming key `main`.

Now, you should be able to access the stream at the following location:

```
http://localhost:8080/hls/main.m3u8
```

Note that it can take a short time for the stream .m3u8 file to be generated,
and so your media player may thow a 404 error before the stream is fully
ingested.

To stop the stream, type:

```
do stream stop
```

---

## Technical specifications

You may have observed that the RTMP stream path is formatted like:

```
rtmp://<your address>:[rtmpPort]/[rtmpStreamName]/
```

Similarly, the HLS stream is formatted like:

```
http://<your address>:8080[hlsStreamPath]/hls/<your stream key>.m3u8
```

The attributes in these formats can be changed through your configuration
parameters.