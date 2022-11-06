from django.shortcuts import render
from django.conf import settings

# Create your views here.
#example api query
# see more at https://nzbgeek.info/dashboard.php?api_generator
'https://api.nzbgeek.info/api?t=movie&imdbid=00067992&limit=50&offset=0&apikey=' + settings.NZBGEEK_APIKEY

# returns xml
# <rss>
#   <channel>
#       <newznab:response offset="0" total="36"/>
#       <item>
#       <title>Willy.Wonka.and.the.Chocolate.Factory.1971.BluRay.720p.DTS.x264.dxva-FLAWL3SS</title>
#       <guid isPermaLink="true">https://nzbgeek.info/geekseek.php?guid=d20e1e2c2591a4b4dc16c94ca28e46b8</guid>
#       <link>https://api.nzbgeek.info/api?t=get&id=d20e1e2c2591a4b4dc16c94ca28e46b8&apikey=NmksXYuEnl4njzlV0jWqlHqJ9bn3o29O</link>
#       <comments>https://nzbgeek.info/geekseek.php?guid=d20e1e2c2591a4b4dc16c94ca28e46b8</comments>
#       <pubDate>Thu, 07 Jul 2022 20:24:21 +0000</pubDate>
#       <category>Movies > BluRay</category>
#       <description>Willy.Wonka.and.the.Chocolate.Factory.1971.BluRay.720p.DTS.x264.dxva-FLAWL3SS</description>
#       <enclosure url="https://api.nzbgeek.info/api?t=get&id=d20e1e2c2591a4b4dc16c94ca28e46b8&apikey=NmksXYuEnl4njzlV0jWqlHqJ9bn3o29O" length="5368927000" type="application/x-nzb"/>
#       <newznab:attr name="category" value="2000"/>
#       <newznab:attr name="category" value="2050"/>
#       <newznab:attr name="size" value="5368927000"/>
#       <newznab:attr name="guid" value="d20e1e2c2591a4b4dc16c94ca28e46b8"/>
#       </item>