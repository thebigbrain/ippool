import 'package:dio/dio.dart';
import 'package:html/parser.dart' show parse;
import 'package:scrapy/scrapy.dart';

import 'items.dart';

class IppoolSpider extends Spider<Quote, Quotes> {
  Stream<String> Parse(Response response) async* {
    var document = parse(response.data.toString());
    var nodes = document.querySelectorAll("div.quote> span.text");

    for (var node in nodes) {
      yield node.innerHtml;
    }
  }

  @override
  Stream<String> Transform(Stream<String> stream) async* {
    await for (String parsed in stream) {
      var transformed = parsed;
      yield transformed.substring(1, parsed.length - 1);
    }
  }

  @override
  Stream<Quote> Save(Stream<String> stream) async* {
    await for (String transformed in stream) {
      Quote quote = Quote(quote: transformed);
      yield quote;
    }
  }

  @override
  void save_result() {
    // TODO: implement save_result
    super.save_result();
  }
}

main() async {
  IppoolSpider spider = IppoolSpider();
  spider.name = "ippool";
  spider.start_urls = ["https://www.xicidaili.com/nn/"];

  Stopwatch stopw = new Stopwatch()..start();

  await spider.start_requests();
  await spider.save_result();

  var elapsed = stopw.elapsed;

  print("the program took $elapsed");
}
