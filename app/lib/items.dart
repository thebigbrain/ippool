import 'package:scrapy/scrapy.dart';

class IpProxy extends Item {
  String ip;
  String port;
  String location;
  String protocol;

  IpProxy({this.ip, this.port, this.location, this.protocol});

  @override
  String toString() {
    return "Proxy : { ip : $ip, port: $port, location: $location, protocol: $protocol }";
  }

  Map<String, dynamic> toJson() =>
      {'ip': ip, 'port': port, 'location': location, 'protocol': protocol};
}

class IpProxies<IpProxy> extends Items {
  @override
  Map<String, dynamic> toJson() {
    return super.toJson();
  }
}
