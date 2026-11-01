// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * QUESTION 4 (BT):
 * Write a program in Solidity to create Student data using structures,
 * arrays and a fallback function. Deploy it on Ethereum and observe the
 * transaction fee and gas values.
 *
 * HOW IT WORKS
 *   struct Student packs one student record: id, name, course and age.
 *   Student[] students is a dynamic array that stores every record.
 *   mapping(uint256 => uint256) indexOf maps a student id to its position
 *   in the array plus one, so id 0 can mean "not found" without a second
 *   lookup loop.
 *
 *   addStudent() pushes a new struct into the array.
 *   getStudent() / getAllStudents() read records (view calls are free).
 *   updateStudent() changes the fields of an existing record.
 *   removeStudent() swaps the record with the last one and pops the array,
 *   which keeps removal O(1).
 *
 *   receive() accepts plain ETH with empty calldata.
 *   fallback() accepts ETH sent with unknown function data, records the raw
 *   calldata and emits an event. This is the fallback requirement of the
 *   assignment.
 *
 * GAS / COST NOTES
 *   Adding a student writes a new struct plus one mapping entry, so it is
 *   the most expensive write (roughly 100k+ gas depending on string length).
 *   Reading is free with eth_call. Sending ETH through receive/fallback
 *   costs about 25k-50k gas plus the calldata cost. In Remix, open the
 *   transaction in the console to see gas used; on Etherscan the fee is
 *   gasUsed * gasPrice (base fee + priority fee).
 *
 * DEPLOY
 *   Remix IDE -> Solidity compiler 0.8.20 or newer -> Deploy & Run ->
 *   Injected Provider (MetaMask) -> Sepolia -> Deploy.
 */
contract StudentData {
    struct Student {
        uint256 id;
        string name;
        string course;
        uint256 age;
    }

    Student[] private students;
    mapping(uint256 => uint256) private indexOf;

    uint256 public totalDonations;
    bytes public lastFallbackData;
    address public lastFallbackSender;

    event StudentAdded(uint256 indexed id, string name, uint256 position);
    event StudentUpdated(uint256 indexed id, string name);
    event StudentRemoved(uint256 indexed id);
    event Received(address indexed sender, uint256 amount);
    event FallbackReceived(address indexed sender, uint256 amount, bytes data);

    error StudentAlreadyExists(uint256 id);
    error StudentNotFound(uint256 id);
    error InvalidStudentData();

    function addStudent(uint256 id, string calldata name,
                        string calldata course, uint256 age) external {
        if (indexOf[id] != 0) revert StudentAlreadyExists(id);
        if (bytes(name).length == 0 || bytes(course).length == 0 || age == 0) {
            revert InvalidStudentData();
        }

        students.push(Student(id, name, course, age));
        indexOf[id] = students.length;

        emit StudentAdded(id, name, students.length - 1);
    }

    function getStudent(uint256 id) external view returns (Student memory) {
        uint256 slot = indexOf[id];
        if (slot == 0) revert StudentNotFound(id);
        return students[slot - 1];
    }

    function getAllStudents() external view returns (Student[] memory) {
        return students;
    }

    function studentCount() external view returns (uint256) {
        return students.length;
    }

    function updateStudent(uint256 id, string calldata name,
                           string calldata course, uint256 age) external {
        uint256 slot = indexOf[id];
        if (slot == 0) revert StudentNotFound(id);
        if (bytes(name).length == 0 || bytes(course).length == 0 || age == 0) {
            revert InvalidStudentData();
        }

        Student storage student = students[slot - 1];
        student.name = name;
        student.course = course;
        student.age = age;

        emit StudentUpdated(id, name);
    }

    function removeStudent(uint256 id) external {
        uint256 slot = indexOf[id];
        if (slot == 0) revert StudentNotFound(id);

        uint256 position = slot - 1;
        uint256 lastPosition = students.length - 1;

        if (position != lastPosition) {
            students[position] = students[lastPosition];
            indexOf[students[position].id] = position + 1;
        }

        students.pop();
        delete indexOf[id];

        emit StudentRemoved(id);
    }

    receive() external payable {
        totalDonations += msg.value;
        emit Received(msg.sender, msg.value);
    }

    fallback() external payable {
        totalDonations += msg.value;
        lastFallbackData = msg.data;
        lastFallbackSender = msg.sender;

        emit FallbackReceived(msg.sender, msg.value, msg.data);
    }
}

// END OF CONTRACT
// The array stores full structs, indexOf gives O(1) id lookup, and the
// swap-and-pop removal avoids shifting every later element. The fallback is
// payable so unknown calls with ETH are recorded instead of reverting.
