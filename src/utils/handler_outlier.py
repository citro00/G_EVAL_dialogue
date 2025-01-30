def handler_outlier(responses):
    handled_response = []
    for score in responses:
        try:
            score = int(score)
            if score > 5:
                score = 5
            elif score < 1:
                score = 1
                
            handled_response.append(score)
        except Exception as e:
            continue
    return handled_response