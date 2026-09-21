from app.duplicate_detector import DuplicateDetector


def test_duplicate_detection():

    detector = DuplicateDetector(
        threshold=0.5
    )

    tickets = [
        {
            "id": "T001",
            "text": "wifi is not working"
        },
        {
            "id": "T002",
            "text": "printer is broken"
        }
    ]

    detector.fit(tickets)

    result = detector.detect(
        "wifi is not working"
    )

    assert result["is_duplicate"] is True
    assert result["matched_ticket_id"] == "T001"