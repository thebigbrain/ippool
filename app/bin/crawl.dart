import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:html/parser.dart' show parse;
import 'package:leveldb/leveldb.dart';
import 'package:scrapy/scrapy.dart';

import 'items.dart';

class IppoolSpider extends Spider<IpProxy, IpProxies> {
  LevelDB<String, String> db;

  IppoolSpider({this.db});

  Stream<String> Parse(Response response) async* {
    var document = parse(response.data.toString());
    var ipList = document.getElementById('ip_list');

    for (var tr in ipList.querySelectorAll('tr').skip(1)) {
      yield tr.querySelectorAll('td').map((td) {
        return td.text.trim();
      }).join(',');
    }
  }

  @override
  Stream<String> Transform(Stream<String> stream) async* {
    await for (String parsed in stream) {
      yield parsed;
    }
  }

  @override
  Stream<IpProxy> Save(Stream<String> stream) async* {
    await for (String transformed in stream) {
      List<String> data = transformed.split(',').sublist(1);
      IpProxy p = IpProxy(
          ip: data[0], port: data[1], location: data[2], protocol: data[4]);
      db.put('${p.protocol}://${p.ip}:${p.port}', jsonEncode(p));
      yield p;
    }
  }

  @override
  void save_result() {
    // TODO: implement save_result
    Items ipList = new Items(items: cache);
    print(jsonEncode(ipList));
  }
}

main() async {
  final LevelDB<String, String> db =
      await LevelDB.openUtf8("/home/localhost/ippool.ldb");

  IppoolSpider spider = IppoolSpider(db: db);
  spider.name = "ippool";
  spider.start_urls = ["https://www.xicidaili.com/nn/"];

  Stopwatch stopw = new Stopwatch()..start();

  await spider.start_requests();
  await spider.save_result();

  var elapsed = stopw.elapsed;

  print("the program took $elapsed");
}
