import { MimeType, TemplateHandler } from 'easy-template-x';
import * as fs from 'fs';

function getMimeType(format) {
    let type = null;
    switch (format) {
        case "png":
            type = MimeType.Png;
            break;
        case "jpg":
            type = MimeType.Jpeg;
            break;
        case "bmp":
            type = MimeType.Bmp;
            break;
        case "gif":
            type = MimeType.Gif;
            break;
        default:
            type = MimeType.Jpeg;
            break
    }
    return type;
}

try {
    const args = process.argv;
    const templateFilename = args[2];
    const dataFilename = args[3];
    const imageFilenames = args[4];
    const outputFilename = args[5];

    // console.log("Templating from " + templateFilename);
    // console.log("Templating with " + dataFilename);
    // console.log("Image definitions in " + imageFilenames);

    const templateFile = fs.readFileSync(templateFilename);
    const images = JSON.parse(fs.readFileSync(imageFilenames, "utf8"));
    var data = JSON.parse(fs.readFileSync(dataFilename, "utf8"));

    for (let image in images) {
        if (images.hasOwnProperty(image)) {
            let imageObject = images[image];

            data[image] = {
                _type: "image",
                width: imageObject.width,
                height: imageObject.height,
                format: getMimeType(imageObject.format),
                source: fs.readFileSync(imageObject.source),
            }
        }
    }

    const handler = new TemplateHandler();
    const doc = await handler.process(templateFile, data);

    fs.writeFileSync(outputFilename, doc);
} catch (exception) {
    console.log("ERROR: ", exception)
}