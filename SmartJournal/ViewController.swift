//
//  ViewController.swift
//  SmartJournal
//
//  Created by 5. 3 on 17/12/2024.
//

import UIKit

class ViewController: UIViewController {

    
    
    @IBOutlet weak var resultLabel: UILabel!
    @IBOutlet weak var textView: UITextView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        resultLabel.text = ""
    }
    
    @IBAction func analyzeButtonTapped(_ sender: UIButton) {
        guard let text = textView.text, !text.isEmpty else {
            resultLabel.text = "Please enter the text"
            return
        }
        
        let url = URL(string: "http:/127.0.0.1:8000/analyze")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let requestBody: [String: Any] = ["text": text]
        request.httpBody = try? JSONSerialization.data(withJSONObject: requestBody)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.resultLabel.text = "Error: /(error.localizedDescription)"
                }
                return
            }
            
            if let data = data,
               let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let analysis = json["analysis"] as? String {
                DispatchQueue.main.async {
                    self.resultLabel.text = analysis
                }
            } else {
                DispatchQueue.main.async {
                    self.resultLabel.text = "Data processing error"
                }
            }
        } .resume()
    }
}

