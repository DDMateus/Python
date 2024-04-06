from sync_folders import calculate_checksum

# Test calculate_checksum function with a valid file
def test_calculate_checksum_with_valid_file():
    sample_file = "sample.txt"
    expected_checksum = "A591A6D40BF420404A011733CFB7B190D62C65BF0BCDA32B57B277D9AD9F146E".lower()

    # Perform the operation
    actual_checksum = calculate_checksum(sample_file)

    # Assert the result
    assert actual_checksum == expected_checksum, "actual_checksum should be equal to expected_checksum"

if __name__ == "__main__":
    test_calculate_checksum_with_valid_file()
    print("Test passed.")
