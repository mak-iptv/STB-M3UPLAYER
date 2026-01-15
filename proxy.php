<?php
header("Access-Control-Allow-Origin: *");

$portal = $_GET['portal'] ?? '';
$mac = $_GET['mac'] ?? '';
$type = $_GET['type'] ?? '';
$action = $_GET['action'] ?? '';
$stream_id = $_GET['stream_id'] ?? '';
$play_token = $_GET['play_token'] ?? 'cra73usMxk'; // mund ta bësh dinamike

if(empty($portal) || empty($mac)){
    echo json_encode(["error"=>"Missing parameters"]);
    exit;
}

// **Nëse po luan kanal** transmet HLS përmes serverit
if($stream_id){
    $url = $portal."/play/live.php?mac=".$mac."&stream=".$stream_id."&extension=m3u8&play_token=".$play_token;

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "User-Agent: Mozilla/5.0 (QtEmbedded; MAG250)",
        "X-User-Agent: Model: MAG250",
        "Cookie: mac=$mac; stb_lang=en; timezone=Europe/London"
    ]);
    $hlsStream = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if($httpCode == 200){
        header("Content-Type: application/vnd.apple.mpegurl");
        echo $hlsStream;
    } else {
        http_response_code($httpCode);
        echo "Error fetching stream";
    }
    exit;
}

// **Nëse po merr listën e kanaleve**
if(empty($type) || empty($action)){
    echo json_encode(["error"=>"Missing parameters"]);
    exit;
}

$url = $portal."/portal.php?type=$type&action=$action";
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "User-Agent: Mozilla/5.0 (QtEmbedded; MAG250)",
    "X-User-Agent: Model: MAG250",
    "Cookie: mac=$mac; stb_lang=en; timezone=Europe/London"
]);
$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response,true);

// Mapping tv_genre_id → emër opsional
$genreMap = [1=>"News",2=>"Movies",3=>"Sports",4=>"Kids",5=>"Music"];

if($type=="itv" && $action=="get_all_channels" && isset($data['js']['data'])){
    $channelsByGroup = [];
    foreach($data['js']['data'] as $ch){
        $group = $ch['category_name'] 
                ?? ($ch['tv_genre_id'] && isset($genreMap[$ch['tv_genre_id']]) ? $genreMap[$ch['tv_genre_id']] : "Genre ".$ch['tv_genre_id'] ?? "Other");
        if(!isset($channelsByGroup[$group])) $channelsByGroup[$group]=[];

        $channelsByGroup[$group][] = [
            "id" => $ch['id'] ?? null,
            "name" => $ch['name'] ?? "NoName",
            "cmd" => $_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']."?stream_id=".$ch['id']."&mac=".$mac."&portal=".$portal."&play_token=".$play_token,
            "logo" => $ch['logo'] ?? ""
        ];
    }
    echo json_encode(["success"=>true,"channels"=>$channelsByGroup]);
    exit;
}

echo $response;
?>
