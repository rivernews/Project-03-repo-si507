/**
 * API
 * 
 * props := {
 *      fields: [
 *          {
 *              label: string,
 *              type: "string",
 *              default?: string,
 *          },
 *          {
 *              label: string,
 *              type: "dropdown",
 *              options: [
 *                  id: string,
 *                  text: string
 *              ],
 *          },
 *      ]
 * }
 * 
 */

class Form {
    constructor(props) {
        this.dom = document.createElement("div");
        this.fields = [];

        // setup props
        let {formID, fields} = props;
        formID = formID || `form-${Math.floor(Math.random() * Math.pow(10, 6))}`;

        // setup fields DOM
        for (let field of fields) {
            let {label, type} = field;
            let fieldID = `${formID}__${label}`;
            let fieldInputID = `${fieldID}__input`;

            let fieldInputDom = null;
            let fieldData = null;
            
            // setup field label DOM
            let labelDom = document.createElement("label");
            labelDom.setAttribute('for', fieldInputID);
            labelDom.innerText = `${label}: `;

            // setup input field dom
            if (type === "string") {
                fieldInputDom = document.createElement("input");
                fieldInputDom.setAttribute('id', fieldInputID);
                fieldInputDom.setAttribute('type', 'text');
                fieldInputDom.value = field.default || ""
            }
            else if (type === "dropdown") {
                let optionDoms = field.options.map((option) => {
                    let optionDom = document.createElement("option");
                    optionDom.value = option.id
                    optionDom.innerText = option.text
                    return optionDom
                })
                fieldInputDom = document.createElement("select");
                fieldInputDom.append(...optionDoms);
                fieldInputDom.setAttribute('id', fieldInputID);
            }

            // store this UI
            let fieldContainer = document.createElement("div");
            fieldContainer.setAttribute('id', fieldID)
            fieldContainer.appendChild(labelDom)
            fieldContainer.appendChild(fieldInputDom)
            fieldData = {
                dom: fieldContainer,
                label,
                value: fieldInputDom.value
            };
            this.fields.push(fieldData)

            // wire up change callback function
            fieldInputDom.onchange = () => {
                fieldData.value = fieldInputDom.value;
            }     
        }

        // attach all field dom to form
        for (let field of this.fields) {
            this.dom.appendChild(field.dom);
        }
    }

    attachTo(selector) {
        document.querySelector(selector).append(this.dom);
    }

    get(label) {
        return this.fields.find((field) => field.label === label).value;
    }
}