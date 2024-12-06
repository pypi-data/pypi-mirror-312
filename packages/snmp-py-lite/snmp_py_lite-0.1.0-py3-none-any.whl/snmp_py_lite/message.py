import time
from .encoder import *


class SNMPMessage:
    def __init__(self, version, community):
        self.version = version
        self.community = community
        
        self.value_tag = {
            0x02: ASN1Integer,
            0x04: ASN1OctetString,
            0x05: ASN1Null,
            0x06: ASN1Oid,
            0x40: ASN1IpAddress,
            0x41: ASN1Counter32,
            0x42: ASN1Gauge,
            0x43: ASN1TimeTicks,
            0x46: ASN1Counter64,
            0x82: ASN1EndOfMibView
        }
    
    def create_get_request(self, oid):
        return self._format_message_content(oid, 0xA0)
    
    def create_get_next_request(self, oid):
        return self._format_message_content(oid, 0xA1)
    
    def create_get_bulk_request(self, oid, non_repeaters, max_repetitions):
        return self._format_message_content(oid, 0xA5, non_repeaters=non_repeaters, max_repetitions=max_repetitions)
    
    def create_set_request(self, oid, value_type, value):
        return self._format_message_content(oid, 0xA3, value_type=value_type, value=value)
    
    def _format_message_content(self, oid, pdu_tag, **kwargs):
        try:
            version_encoded = ASN1Integer.encode(self.version)
            community_encoded = ASN1OctetString.encode(self.community)
            
            pdu = PDU.create_get_request_pdu(oid, pdu_tag, **kwargs)
            
            message_content = version_encoded + community_encoded + pdu
            return ASN1Tagged.encode(0x30, message_content)
        except Exception as e:
            raise ValueError(f'Message encode operation error. {e}')
    
    def parse_response(self, data):
        self._check_integrity(data)

        list_value = []
        while data:
            decoder_class = self.value_tag.get(data[0])
            
            if decoder_class is None:
                decoder_class = ASN1Tagged()
                _, data = decoder_class.decode(data)
            else:
                value, data = decoder_class.decode(data)
                list_value.append(value)
                
        return list_value
    
    def _check_integrity(self, data):
        if data[0] != 0x30:
            raise ValueError("package is not snmp")
        expected_length, remaining_data = ASN1Element.decode_length(data[1:])
        if len(remaining_data) != expected_length:
            raise ValueError(f"package integrity is broken: {expected_length} byte is expected, but {len(remaining_data)} byte is received")


class PDU:
    def __init__(self):
        self.type_map = {
            'INTEGER': ASN1Integer,
            'i': ASN1Integer,
            
            'STRING': ASN1OctetString,
            's': ASN1OctetString,
            
            'IPADDRESS': ASN1IpAddress,
            'a': ASN1IpAddress,
            
            'COUNTER': ASN1Counter32,
            'c': ASN1Counter32,
            
            'GAUGE': ASN1Gauge,
            'g': ASN1Gauge,
            
            'TIMETICKS': ASN1TimeTicks,
            't': ASN1TimeTicks
        }

    @staticmethod
    def create_get_request_pdu(oid, pdu_tag, **kwargs):
        oid_encoded = ASN1Oid.encode(oid)
        request_id = ASN1Integer.encode(int(time.time() * 161) % 2147483647)

        error_status = ASN1Integer.encode(kwargs.get('non_repeaters', 0))
        error_index = ASN1Integer.encode(kwargs.get('max_repetitions', 0))
        
        if {'value_type', 'value'} <= kwargs.keys():
            value_type = kwargs.get('value_type')
            value = kwargs.get('value')
            encoder_class = PDU().type_map.get(value_type)
            value_encoded = encoder_class.encode(value)
        else:
            value_encoded = ASN1Null.encode()
            
        varbind = VarBind.create_varbind(oid_encoded, value_encoded)
        varbind_list = ASN1Tagged.encode(0x30, varbind)

        pdu_content = request_id + error_status + error_index + varbind_list
        return ASN1Tagged.encode(pdu_tag, pdu_content)


class VarBind:
    @staticmethod
    def create_varbind(oid_encoded, value_encoded):
        varbind_content = oid_encoded + value_encoded
        return ASN1Tagged.encode(0x30, varbind_content)
