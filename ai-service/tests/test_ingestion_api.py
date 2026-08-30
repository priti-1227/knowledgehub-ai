import pymupdf

from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def create_test_pdf(path):

    pdf = pymupdf.open()

    page = pdf.new_page()

    page.insert_text(
        (50, 50),
        """
        Remote Work Policy

        Employees may work remotely up to
        two days per week.

        Manager approval is required.
        """,
    )

    pdf.save(path)

    pdf.close()


def test_ingestion_api(tmp_path):

    pdf_path = (
        tmp_path / "remote_policy.pdf"
    )

    create_test_pdf(
        pdf_path
    )

    response = client.post(
        "/api/v1/documents/ingest",

        json={
            "file_path": str(pdf_path),

            "document_name":
                "Remote Work Policy",

            "department":
                "HR",
        },
    )

    print("\nSTATUS CODE:")
    print(response.status_code)

    print("\nRESPONSE:")
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in (
        "success",
        "duplicate",
    )
    second_response = client.post(
        "/api/v1/documents/ingest",

        json={
            "file_path": str(pdf_path),
            "document_name": "Remote Work Policy",
            "department": "HR",
        },
    )

    second_data = second_response.json()

    print("\nSECOND INGESTION:")
    print(second_data)

    assert second_data["status"] == "duplicate"